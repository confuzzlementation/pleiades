from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import xgboost as xgb
import numpy as np
import pickle
import os

app = Flask(__name__)
CORS(app)

model = None
feature_columns = None


def train_and_save_model():
    global feature_columns

    data = pd.read_csv("data.csv")
    data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0)
    X, Y = data.iloc[:, :-1], data.iloc[:, -1]

    feature_columns = X.columns.tolist()

    dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)

    params = {
        "objective": "reg:logistic",
        "max_depth": 50,
        "learning_rate": 0.50,
        "alpha": 5,
    }

    model = xgb.train(params=params, dtrain=dmatrix, num_boost_round=1000)

    model.save_model("xgb_model.json")
    with open("feature_columns.pkl", "wb") as f:
        pickle.dump(feature_columns, f)

    print("Model trained and saved successfully.")
    return model


def load_model():
    global model, feature_columns

    if os.path.exists("xgb_model.json") and os.path.exists("feature_columns.pkl"):
        model = xgb.Booster()
        model.load_model("xgb_model.json")

        with open("feature_columns.pkl", "rb") as f:
            feature_columns = pickle.load(f)

        print("Model loaded successfully.")
    else:
        print("Model files not found. Training new model...")
        model = train_and_save_model()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        df = pd.DataFrame([data])

        missing_features = set(feature_columns) - set(df.columns)
        if missing_features:
            return (
                jsonify({"error": f"Missing features: {list(missing_features)}"}),
                400,
            )

        df = df[feature_columns]

        dmatrix = xgb.DMatrix(df, enable_categorical=True)

        prediction = model.predict(dmatrix)[0]

        return jsonify(
            {
                "prediction": float(prediction),
                "class": "CANDIDATE" if prediction > 0.5 else "FALSE POSITIVE",
                "confidence": (
                    float(prediction) if prediction > 0.5 else float(1 - prediction)
                ),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json()

        if not data or not isinstance(data, list):
            return jsonify({"error": "Expected array of feature dictionaries"}), 400

        df = pd.DataFrame(data)

        missing_features = set(feature_columns) - set(df.columns)
        if missing_features:
            return (
                jsonify({"error": f"Missing features: {list(missing_features)}"}),
                400,
            )

        df = df[feature_columns]

        dmatrix = xgb.DMatrix(df, enable_categorical=True)

        predictions = model.predict(dmatrix)

        results = [
            {
                "prediction": float(pred),
                "class": "CANDIDATE" if pred > 0.5 else "FALSE POSITIVE",
                "confidence": float(pred) if pred > 0.5 else float(1 - pred),
            }
            for pred in predictions
        ]

        return jsonify({"predictions": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/features", methods=["GET"])
def get_features():
    return jsonify({"features": feature_columns, "count": len(feature_columns)})


@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        global model
        model = train_and_save_model()
        return jsonify({"message": "Model retrained successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    load_model()
    app.run(debug=True, host="0.0.0.0", port=5000)
