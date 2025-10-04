from flask import Blueprint, jsonify, current_app

model_bp = Blueprint("model", __name__)


@model_bp.route("/features", methods=["GET"])
def get_features():
    model_manager = current_app.config["MODEL_MANAGER"]
    return jsonify(
        {
            "features": model_manager.feature_columns,
            "count": (
                len(model_manager.feature_columns)
                if model_manager.feature_columns
                else 0
            ),
        }
    )


@model_bp.route("/retrain", methods=["POST"])
def retrain():
    try:
        model_manager = current_app.config["MODEL_MANAGER"]
        model_manager.train_and_save_model()
        return jsonify({"message": "Model retrained successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
