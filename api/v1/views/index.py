#!/usr/bin/python3
"""The index file for the api folder"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    """Give the status in a JSON format"""
    return jsonify({'status': 'OK'})
