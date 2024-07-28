#!/usr/bin/python3
"""Flask web application for AirBnB clone"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """Display a HTML page with the list of all State objects"""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Display a HTML page with the cities of a specific State"""
    states = storage.all(State)
    state = states.get(f"State.{id}")
    if state:
        return render_template('9-states.html', state=state)
    return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
