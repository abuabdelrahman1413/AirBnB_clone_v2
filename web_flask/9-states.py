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


@app.route('/states/<id>', strict_slashes=False)
@app.route('/states', strict_slashes=False)
def state_cities(id=None):
    state_dict = storage.all(State).values()
    if (id is not None):
        key = 'State.{}'.format(id)
        if key in storage.all(State).keys():
            state = storage.all(State)[key]
        else:
            state = "NotFound"
        idflag = 1
    else:
        state = None
        idflag = 0
    return render_template('9-states.html', states=state_dict,
                           idflag=idflag, state=state)


@app.teardown_appcontext
def close_sess(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
