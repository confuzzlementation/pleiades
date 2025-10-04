import pandas as pd
import xgboost as xgb
import pickle
import os
from threading import Lock


class ModelManager:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.lock = Lock()
        self.model_path = "xgb_model.json"
        self.features_path = "feature_columns.pkl"

    def train_and_save_model(self):
        with self.lock:
            data = pd.read_csv("data.csv")
            groups = data["kepid"]
            data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0)
            X, Y = data.iloc[:, :-1], data.iloc[:, -1]

            self.feature_columns = X.columns.tolist()

            dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)

            params = {
                "objective": "binary:logistic",
                "max_depth": 50,
                "learning_rate": 0.50,
                "alpha": 5,
            }

            self.model = xgb.train(params=params, dtrain=dmatrix, num_boost_round=1000, early_stopping_rounds=500)

            self.model.save_model(self.model_path)
            with open(self.features_path, "wb") as f:
                pickle.dump(self.feature_columns, f)

            print("Model trained and saved successfully!")
            return self.model

    def load_model(self):
        with self.lock:
            if os.path.exists(self.model_path) and os.path.exists(self.features_path):
                self.model = xgb.Booster()
                self.model.load_model(self.model_path)

                with open(self.features_path, "rb") as f:
                    self.feature_columns = pickle.load(f)

                print("Model loaded successfully!")
            else:
                print("Model files not found. Training new model...")
                self.train_and_save_model()

    def predict(self, df):
        with self.lock:
            if self.model is None:
                raise ValueError("Model not loaded")

            # Validate features
            missing_features = set(self.feature_columns) - set(df.columns)
            if missing_features:
                raise ValueError(f"Missing features: {list(missing_features)}")

            df = df[self.feature_columns]

            dmatrix = xgb.DMatrix(df, enable_categorical=True)

            return self.model.predict(dmatrix)
