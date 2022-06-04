from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "its_a_secret_to_everybody"

debug = DebugToolbarExtension(app)
