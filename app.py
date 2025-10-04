from flask import Flask
from flask_cors import CORS
from routes.prediction_routes import prediction_bp
from routes.model_routes import model_bp
from utils.model_manager import ModelManager

app = Flask(__name__)
CORS(app)

model_manager = ModelManager()

app.config["MODEL_MANAGER"] = model_manager

app.register_blueprint(prediction_bp, url_prefix="/api")
app.register_blueprint(model_bp, url_prefix="/api")


@app.route("/health", methods=["GET"])
def health_check():
    from flask import jsonify

    return jsonify(
        {"status": "healthy", "model_loaded": model_manager.model is not None}
    )


if __name__ == "__main__":
    model_manager.load_model()

    app.run(debug=True, host="0.0.0.0", port=5000)
