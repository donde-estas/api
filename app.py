import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from helpers.keys import generate_random_key

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from person import Person


@app.route("/")
def hello():
    return "Bienvenido a Dónde Estás!"


@app.route("/missing", methods=['GET'])
def get_all_missing():
    try:
        return jsonify({
            'success': True,
            'payload': [x.serialize() for x in Person.query.all()]
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/missing", methods=['POST'])
def create_new_missing():
    """Creates a missing person in the database."""
    try:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        missing_number = request.args.get('missing_number')
        contact_number = request.args.get('contact_number')
        plain_key = generate_random_key()

        person = Person(first_name, last_name, plain_key)

        db.session.add(person)
        db.session.commit()
        return jsonify({
            'success': True,
            'payload': {
                'plain_key': plain_key,
                'person': person.serialize()
            }
        }), 201
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/missing/<int:id_>", methods=['GET'])
def get_missing(id_):
    try:
        person = Person.query.filter_by(id=id_).first()
        if not person:
            return jsonify({
                'success': False,
                'payload': 'Person does not exist in the database (invalid id)'
            }), 404

        return jsonify({
            'success': True,
            'payload': person.serialize()
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/missing/<int:id_>", methods=['DELETE'])
def delete_missing(id_):
    try:
        person = Person.query.filter_by(id=id_).first()
        plain_key = request.args.get('plain_key')
        if not person:
            return jsonify({
                'success': False,
                'payload': 'Person does not exist in the database (invalid id)'
            }), 404
        if not person.check_plain_key(plain_key):
            return jsonify({
                'success': False,
                'payload': 'Invalid auth key'
            }), 401
        db.session.delete(person)
        db.session.commit()
        return jsonify({
            'success': True,
            'payload': "Person removed successfully"
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/missing/<int:id_>", methods=['PATCH'])
def find_missing(id_):
    try:
        person = Person.query.filter_by(id=id_).first()
        plain_key = request.args.get('plain_key')
        if not person:
            return jsonify({
                'success': False,
                'payload': 'Person does not exist in the database (invalid id)'
            }), 404
        if person.found:
            return jsonify({
                'success': False,
                'payload': "Person has already been found"
            }), 409
        if not person.check_plain_key(plain_key):
            return jsonify({
                'success': False,
                'payload': 'Invalid auth key'
            }), 401
        if person.set_as_found():
            db.session.commit()
            return jsonify({
                'success': True,
                'payload': "Person found successfully"
            }), 200
        else:
            return jsonify({
                'success': False,
                'payload': "Unexpected internal server state change"
            }), 409
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


if __name__ == '__main__':
    app.run()
