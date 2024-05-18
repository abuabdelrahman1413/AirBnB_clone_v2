#!/usr/bin/python3
"""This module starts a Flask webb application
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_sess(exception=None):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    state_dict = storage.all(State)
    str_dict = []
    for key, value in state_dict.items():
        str_dict.append(value.to_dict())
    print(str_dict)
    return render_template('7-states_list.html', objects=str_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
