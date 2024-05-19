#!/usr/bin/python3
"""This module starts a Flask webb application
"""
from flask import Flask, render_template
from models import storage
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)



@app.teardown_appcontext
def close_sess(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
