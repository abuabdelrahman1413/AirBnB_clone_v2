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


@app.teardown_appcontext
def close_sess(exception=None):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    state_dict = storage.all(State)
    str_dicts = []
    for key, value in state_dict.items():
        str_dicts.append(value.to_dict())
    return render_template('7-states_list.html', objects=str_dicts)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
