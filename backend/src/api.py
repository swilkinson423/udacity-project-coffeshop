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





def get_drinks(recipe_format):
# THIS IS CONVERTED FROM GITHUB CODE!!!!!!!!!!!!
# SOURCE: https://github.com/Thalrion/Udacity-Full-Stack-Developer-Nanodegree/blob/master/project03_coffee_shop/finished/backend/src/api.py

    all_drinks = Drink.query.order_by(Drink.id).all()

    # Get recipe detail format
    if recipe_format.lower() == 'short':
        all_drinks_formatted = [drink.short() for drink in all_drinks]
    elif recipe_format.lower() == 'long':
        all_drinks_formatted = [drink.long() for drink in all_drinks]
    else:
        return abort(500)

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'no drinks found in database.'})

    return all_drinks_formatted


#------------------------------------------------------#
# Endpoint Routes
#------------------------------------------------------#

# GET /drinks
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def drinks(payload):

    return jsonify({
        'success':True,
        'drinks':get_drinks('short')
    })


# GET /drinks-detail
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):

    return jsonify({
        'success':True,
        'drinks':get_drinks('long')
    })


# POST /drinks
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):

    body = request.get_json()
    drink = Drink(
        title = body['title'],
        recipe = """{}""".format(body['recipe'])
    )

    drink.insert()
    drink.recipe = body['recipe']

    return jsonify({
        'success':True,
        'drinks': Drink.long(drink)
    })


# PATCH /drinks/<drink_id>
@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload):

    body = request.get_json()

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    title_new = body.get('title', None)
    recipe_new = body.get('recipe', None)

    if title_new:
        drink.title = body['title']

    if recipe_new:
        drink.recipe = """{}""".format(body['recipe'])

    drink.update()

    return jsonify({
        'success':True,
        'drinks': [Drink.long(drink)]
    })


# DELETE /drinks/<drink_id>
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload):

    if not drink_id:
        abort(422)

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    drink.delete()

    return jsonify({
        'success':True,
        'delete':drink_id
    })


#------------------------------------------------------#
# Error Handlers
#------------------------------------------------------#

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

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

@app.errorhandler(AuthError)
def authentication_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error
    }), 401

@app.errorhandler(500)
def bad_format_request(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Wrong format. Format needs to be "short" or "long".'
    }), 500