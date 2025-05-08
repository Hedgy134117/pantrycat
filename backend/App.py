from flask import Flask, jsonify
from flask_cors import CORS

from PantryCat import PantryCat

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def recipes():
    pc = PantryCat(False)
    recipes = pc.get_recipes()
    pc.close()
    return jsonify(recipes)


@app.route("/<ingredient>")
def recipes_with_ingredient(ingredient: str):
    pc = PantryCat(False)
    recipes = pc.get_recipes_using(ingredient)
    pc.close()
    return jsonify(recipes)
