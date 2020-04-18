
# Here is the api flask server runner for PFC game.

from flask import Flask
from flask import render_template
import pickle
import os.path

app = Flask(__name__)

@app.route('/')
def first_players():
    with open("data.cornichon", "rb") as f:
        data = pickle.load(f)
        return render_template("first_players.html", players=data.ranking[:3])
