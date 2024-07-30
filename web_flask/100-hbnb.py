#!/usr/bin/python3
"""
Flask application that defines the routes for the AirBnB clone
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays the HBNB page"""
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    reviews = storage.all(Review).values()
    users = storage.all(User).values()
    return render_template('100-hbnb.html',
                           states=states, cities=cities,
                           amenities=amenities, places=places,
                           reviews=reviews, users=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
