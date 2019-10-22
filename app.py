import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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



if __name__ == '__main__':
    app.run()
