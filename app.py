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
def missing():
    try:
        return jsonify({'success': True, 'payload': Person.query.all()})
    except Exception as error:
        return jsonify({'success': False, 'payload': str(error)})


@app.route("/missing", methods=['POST'])
def missing():
    """Creates a missing person in the database."""
    try:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        phone_number = request.args.get('phone_number')
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



if __name__ == '__main__':
    app.run()
