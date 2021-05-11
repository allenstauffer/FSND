import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()


def get_drinks_short():
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    return [drink.short() for drink in drinks]


def get_drinks_long():
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    return [drink.long() for drink in drinks]


# ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    return jsonify({
        'success': True,
        'drinks': get_drinks_short()
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    return jsonify({
        'success': True,
        'drinks': get_drinks_long()
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def get_drinks_post(payload):
    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        if title is None or recipe is None:
            abort(401)
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        drink.insert()
        returnArray = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': returnArray
        })
    except Exception:
        print(sys.exc_info())
        abort(422)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def get_drinks_patch(payload, id):
    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe)
        drink.update()
        returnArray = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': returnArray
        })
    except Exception:
        print(sys.exc_info())
        abort(422)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def get_drinks_delete(payload, id):
    try:
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)

        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception:
        print(sys.exc_info())
        abort(422)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404


@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error['description']
        }), AuthError.status_code
