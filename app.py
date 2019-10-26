import os
import re
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from custom_exceptions import EmptyNameError, InvalidMailError
from helpers import generate_random_key, dispatch_mail
import templates

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from person import Person

MAIL_TESTER = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


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


@app.route("/person", methods=['GET'])
def get_every_person():
    try:
        return jsonify({
            'success': True,
            'payload': [x.serialize() for x in Person.query.all()]
        }), 200
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)}), 503


@app.route("/person", methods=['POST'])
def create_person():
    """Creates a missing person in the database."""
    try:
        first_name = request.args.get('first_name').strip()
        last_name = request.args.get('last_name').strip()
        if not first_name or not last_name:
            raise EmptyNameError()
        missing_mail = request.args.get('missing_mail').strip()
        contact_mail = request.args.get('contact_mail').strip()
        if not MAIL_TESTER.match(missing_mail):
            raise InvalidMailError(missing_mail)
        if not MAIL_TESTER.match(contact_mail):
            raise InvalidMailError(contact_mail)
        plain_key = generate_random_key()

        last_seen = False  # request.args.get('last_seen')
        latitude = request.args.get('latitude')
        latitude = float(latitude.strip()) if latitude else None
        longitude = request.args.get('longitude')
        longitude = float(longitude.strip()) if longitude else None

        person = Person(first_name, last_name, missing_mail, contact_mail,
                        plain_key, latitude, longitude, last_seen)

        # Generate mails
        mail_args = {
            'missing_name': f'{first_name} {last_name}',
            'key': plain_key
        }

        # Save Person in the database
        db.session.add(person)
        db.session.commit()

        found_link = (f'{os.environ.get("WEBAPP_URL")}/'
                      f'person/{person.id}/find/{plain_key}')

        missing_s = dispatch_mail(
            missing_mail,
            templates.template,
            templates.initial_missing_body,
            templates.default_style,
            templates.find_person_button.format(
                found_link=found_link,
                message="¡Estoy Bien!"
            ),
            mail_args
        )
        contact_s = dispatch_mail(
            contact_mail,
            templates.template,
            templates.initial_contact_body,
            templates.default_style,
            templates.find_person_button.format(
                found_link=found_link,
                message="¡Apareció!"
            ),
            mail_args
        )

        if missing_s.status_code != 200 and contact_s.status_code != 200:
            # Eliminar a persona de la base de datos
            db.session.delete(person)
            db.session.commit()

            return jsonify({
                'success': False,
                'payload': ('Mailer error occurred, could not deliver '
                            'secret key (Missing person not created)')
            }), max(missing_s.status_code, contact_s.status_code)

        return jsonify({
            'success': True,
            'payload': person.serialize()
        }), 200
    except (EmptyNameError, InvalidMailError) as error:
        return jsonify({'success': False, 'payload': str(error)}), 400
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
