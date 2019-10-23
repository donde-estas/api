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
        })
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)})


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
        })
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)})


@app.route("/missing/<int:id_>", methods=['GET'])
def get_missing(id_):
    try:
        person = Person.query.filter_by(id=id_).first()
        if not person:
            raise Exception("User does not exist in the database (invalid id)")

        return jsonify({
            'success': True,
            'payload': person.serialize()
        })
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)})


@app.route("/missing/<int:id_>", methods=['DELETE'])
def delete_missing(id_):
    try:
        person = Person.query.filter_by(id=id_).first()
        plain_key = request.args.get('plain_key')
        if not person:
            raise Exception("User does not exist in the database (invalid id)")
        if not person.check_plain_key(plain_key):
            raise Exception("Invalid auth key")
        db.session.delete(person)
        db.session.commit()
        return jsonify({
            'success': True,
            'payload': "User removed successfully"
        })
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)})


if __name__ == '__main__':
    app.run()
