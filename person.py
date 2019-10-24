"""This module includes every person model used inside the API."""

from datetime import datetime

from app import app, db

from auxiliary_models import Location
from helpers.keys import generate_key_digest, check_key


class Person(db.Model):

    """Models a person."""

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    mail = db.Column(db.String())
    contact_mail = db.Column(db.String())
    key_digest = db.Column(db.String())
    created_date = db.Column(db.DateTime())
    found = db.Column(db.Boolean())
    found_date = db.Column(db.DateTime())

    last_seen = db.relationship(
        "Location",
        uselist=False,
        back_populates="person"
    )

    def __init__(self, first_name, last_name, mail, contact_mail, plain_key,
                 latitude, longitude, last_seen=False):
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        self.contact_mail = contact_mail
        self.created_date = datetime.utcnow()
        self.found_date = None
        self.last_seen = Location(latitude, longitude, last_seen)
        self.found = False
        self.set_key_digest(plain_key)

    def set_key_digest(self, plain_key):
        """Sets secure key digest."""
        self.key_digest = generate_key_digest(plain_key)

    def check_plain_key(self, plain_key):
        """Checks plain key."""
        return check_key(plain_key, self.key_digest)

    def set_as_found(self):
        """Sets the user as found."""
        if self.found:
            # If it had already been found
            return False
        self.found = True
        self.found_date = datetime.utcnow()
        return True

    def __repr__(self):
        return '<Person - id {}>'.format(self.id)

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            'id': self.id,
            'name': self.first_name,
            'last_name': self.last_name,
            'found': self.found,
            'created_date': self.created_date,
            'found_date': self.found_date,
            'last_seen': self.last_seen.serialize()
        }
