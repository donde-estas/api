import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from helpers import generate_random_key, dispatch_mail
import templates

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
            'payload': [
                x.serialize() for x in Person.query.all() if not x.found
            ]
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


@app.route("/found", methods=['GET'])
def get_all_found():
    try:
        return jsonify({
            'success': True,
            'payload': [x.serialize() for x in Person.query.all() if x.found]
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/person", methods=['POST'])
def create_person():
    """Creates a missing person in the database."""
    try:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        missing_mail = request.args.get('missing_mail')
        contact_mail = request.args.get('contact_mail')
        plain_key = generate_random_key()

        person = Person(first_name, last_name, plain_key)

        # Generate mails
        mail_args = {
            'missing_name': f'{first_name} {last_name}',
            'contact_name': 'Generic Contact Person',
            'find_person_button': templates.find_person_button,
            'key': plain_key
        }
        missing_s = dispatch_mail(
            missing_mail,
            templates.template,
            templates.initial_missing_body,
            templates.default_style,
            mail_args)
        contact_s = dispatch_mail(
            contact_mail,
            templates.template,
            templates.initial_contact_body,
            templates.default_style,
            mail_args)

        if missing_s.status_code != 200 and contact_s.status_code != 200:
            return jsonify({
                'success': False,
                'payload': 'Mailer error, could not deliver secret key'
            }), max(missing_s.status_code, contact_s.status_code)

        # Save Person in the database
        db.session.add(person)
        db.session.commit()

        return jsonify({
            'success': True,
            'payload': person.serialize()
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/person/<int:id_>", methods=['GET'])
def get_person(id_):
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


@app.route("/person/<int:id_>", methods=['DELETE'])
def delete_person(id_):
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


if __name__ == '__main__':
    app.run()
