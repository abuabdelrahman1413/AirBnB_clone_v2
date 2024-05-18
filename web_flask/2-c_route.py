#!/usr/bin/python3
"""This module starts a Flask web application.
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ defines the page to display at '/'
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ defines the page to display at '/hbnb'
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ defines the page to display at '/c/'
    followed by any text
    """
    return "C {}".format(text).replace("_", " ")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
