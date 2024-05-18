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


@app.route('/cities_by_states', strict_slashes=False)
def state_cities():
    state_dict = storage.all(State).values()
    city_dict = {}
    for state in state_dict:
        city_dict[state] = state.cities
    return render_template('8-cities_by_states.html',
                           states=state_dict, cities=city_dict)


@app.teardown_appcontext
def close_sess(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
