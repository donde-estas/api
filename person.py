"""This module includes every person model used inside the API."""

from datetime import datetime, timedelta

from app import app, db

from helpers.keys import generate_key_digest, check_key


class Person(db.Model):

    """Models the user."""

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    key_digest = db.Column(db.String())
    created_date = db.Column(db.DateTime())

    def __init__(self, first_name, last_name, plain_key):
        self.first_name = first_name
        self.last_name = last_name
        self.created_date = datetime.utcnow()
        self.set_key_digest(plain_key)

    def set_key_digest(self, plain_key):
        """Sets secure key digest."""
        self.key_digest = generate_key_digest(plain_key)

    def check_plain_key(self, plain_key):
        """Checks plain key."""
        return check_key(plain_key, self.key_digest)

    def __repr__(self):
        return '<Person - id {}>'.format(self.id)

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            'id': self.id,
            'name': self.first_name,
            'last_name': self.last_name,
            'key_digest': self.key_digest,
            'created_date': self.created_date
        }
