import flask
from flask import Flask
from flask_cors import CORS
from routes.prediction_routes import prediction_bp
from routes.model_routes import model_bp
from utils.model_manager import ModelManager
from flask import render_template
from flask import jsonify

app = Flask(__name__)
CORS(app)

model_manager = ModelManager()

app.config["MODEL_MANAGER"] = model_manager

app.register_blueprint(prediction_bp, url_prefix="/api")
app.register_blueprint(model_bp, url_prefix="/api")


@app.route("/", methods=["GET"])
def displayHome():
    return render_template("home.html")


@app.route("/model", methods=["GET", "POST"])
def displayModel():
    if flask.request.method == "GET":
        return render_template("model.html")
    if flask.request.method == "POST":
        max_depth = flask.request.form["max_depth"]
        # etc. do ^^ for whichever other parameters we end up using
        # return(flask.render_template('main.html', predict_text=predict_text, movie=movie, result=prediction))
        """ 
        follow this for integration? https://blog.bolajiayodeji.com/how-to-deploy-a-machine-learning-model-to-the-web
        add model results like this into the html as well (but change the parameters in the comment above and in this one)
        <div class="result mt-12" align="center">
          <span id="predict_text">{{ predict_text }}</span>
          <span id="selected_movie" class="text-gray-700">{{ movie }}</span>
          <p class="text-blue-700 text-lg font-bold border rounded mt-4">
            {{ result }}
          </p>
        </div>
        """


# @app.route("/adv", methods=["GET"])
# def displayAdvancedModel():
#     return render_template("advmodel.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify(
        {"status": "healthy", "model_loaded": model_manager.model is not None}
    )



if __name__ == "__main__":
    model_manager.load_model()

    app.run(debug=True, host="0.0.0.0", port=3300)