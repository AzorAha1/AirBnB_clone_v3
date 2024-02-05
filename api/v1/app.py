#!/usr/bin/python3
"""an api file for the airbnb"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """a function that calls for the close function"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(exception):
    return jsonify({
        'error': "Not found"
    }), 404


if __name__ == "__main__":
    hostname = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=hostname, port=port, threaded=True)
