#!/usr/bin/python3
"""This module starts a Flask web application.
"""
from flask import Flask, abort, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Defines the page to display at '/'
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Defines the page to display at '/hbnb'
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ Defines the page to display at '/c/'
    followed by any text
    """
    return "C {}".format(text).replace("_", " ")


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """ Defines the page to display at '/python/'
    followed by any text
    """
    return "Python {}".format(text).replace("_", " ")


@app.route('/number/<n>', strict_slashes=False)
def number_n(n):
    """ Defines the page to display at '/number/n'
    if n is a number.
    """
    if (n.isdigit()):
        return "{} is a number".format(n)
    else:
        abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    if (n.isdigit()):
        return render_template('5-number.html', number=n)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
