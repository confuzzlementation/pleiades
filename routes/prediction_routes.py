from flask import Blueprint, request, jsonify, current_app
import pandas as pd

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/predict", methods=["POST"])
def predict():
    try:
        model_manager = current_app.config["MODEL_MANAGER"]

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        df = pd.DataFrame([data])

        prediction = model_manager.predict(df)[0]

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


@prediction_bp.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        model_manager = current_app.config["MODEL_MANAGER"]

        data = request.get_json()

        if not data or not isinstance(data, list):
            return jsonify({"error": "Expected array of feature dictionaries"}), 400

        df = pd.DataFrame(data)

        predictions = model_manager.predict(df)

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
