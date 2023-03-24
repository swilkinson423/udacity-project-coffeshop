import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


#------------------------------------------------------#
# App Setup
#------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)
with app.app_context():
    db_drop_and_create_all()


#------------------------------------------------------#
# Helper Functions
#------------------------------------------------------#







#------------------------------------------------------#
# Endpoint Routes
#------------------------------------------------------#

# GET /drinks
@app.route('/drinks')
@requires_auth('get:drinks')
def drinks(payload):
    
    drinks = ''

    # TODO return drink.short() data as 'drinks' var
    # TODO return proper success/error codes
    
    return jsonify({
        'success':True,
        'drinks':drinks
    })


# GET /drinks-detail
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(payload):

    drinks_detail = ''

    # TODO return drinks.long() data as 'drinks_detail' var
    # TODO return proper success/error codes

    return jsonify({
        'success':True,
        'drinks':drinks_detail
    })


# POST /drinks
@app.route('/drinks')
@requires_auth('post:drinks')
def post_drinks(payload):

    drink = ''

    # TODO check if payload contains drink.long() formatted data for new drink
    # TODO format 'drink' var to be an array containing data from payload
    # TODO return proper success/error codes

    return jsonify({
        'success':True,
        'drinks':drink
    })


# PATCH /drinks/<drink_id>
@app.route('/drinks/<drink_id>')
@requires_auth('patch:drinks')
def update_drink(payload):

    drink = ''

    # TODO check to find drink by 'drink_id'
        # TODO ?? Check if payload contains 'drinks.long()' ??
    # TODO return 404 if ID doesn't exist
    # TODO format 'drink' var to be an array containing data from payload
    # TODO return proper success/error codes

    return jsonify({
        'success':True,
        'drinks':drink
    })


# DELETE /drinks/<drink_id>
@app.route('/drinks/<drink_id>')
@requires_auth('delete:drinks')
def delete_drink(payload):

    drink = ''

    # TODO check to find drink by 'drink_id'
    # TODO return 404 if ID doesn't exist
    # TODO delete record for drink
    # TODO return proper success/error codes

    return jsonify({
        'success':True,
        'delete':drink_id
    })


#------------------------------------------------------#
# Error Handlers
#------------------------------------------------------#

# implement error handlers using the @app.errorhandler(error) decorator

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

# implement error handler for 404

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

# TODO DONE implement error handler for AuthError

@app.errorhandler(AuthError)
def authentication_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error
    }), 401