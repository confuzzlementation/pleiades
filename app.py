import flask
from flask import Flask
from flask_cors import CORS
from routes.prediction_routes import prediction_bp
from routes.model_routes import model_bp
from utils.model_manager import ModelManager
from flask import render_template
from flask import jsonify
from flask import request
import pickle

# # Use pickle to load in the pre-trained model.
# with open(f'model/movie_reviews_sentiment_analysis.pkl', 'rb') as f: # need to change to our file
#     model = pickle.load(f)

# # Use pickle to load in vectorizer.
# with open(f'model/vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)

#alesha you stupid gremlin

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
    if request.method == "GET":
        return render_template("model.html")
    if request.method == "POST":
        max_depth = request.form["max_depth"]
        min_child_weight = request.form["min_child_weight"]
        learning_rate = request.form["learning_rate"]
        subsample = request.form["subsample"]
        colsample_bytree = request.form["colsample_bytree"]
        alpha = request.form["alpha"]
        lmbda = request.form["lambda"]
        orbital_period = request.form["orbital_period"]
        transit_epoch = request.form["transit_epoch"]
        impact_parameter = request.form["impact_parameter"]
        transit_duration_hours = request.form["transit_duration_hours"]
        transit_depth_ppm = request.form["transit_depth_ppm"]
        planet_star_ratio = request.form["planet_star_ratio"]
        stellar_density = request.form["stellar_density"]
        planet_radius = request.form["planet_radius"]
        semi_major_axis = request.form["semi_major_axis"]
        inclination = request.form["inclination"]
        insolation_flux = request.form["insolation_flux"]
        limb_darkening_1 = request.form["limb_darkening_1"]
        limb_darkening_2 = request.form["limb_darkening_2"]

        prediction = model.predict(vectorizer.transform([review]))
        return(flask.render_template('main.html', result=result))
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