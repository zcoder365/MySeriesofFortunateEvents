# imports
from flask import Flask, render_template, request, redirect, session, flash, url_for
import utils.model as model
import utils.database as db

# prep the app and add configurations
app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=5001, debug=True)