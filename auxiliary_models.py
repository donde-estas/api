"""This module includes every aux model used inside the API."""

from app import app, db


class Location(db.Model):

    """Models a location."""

    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    existent = db.Column(db.Boolean())

    person_id = db.Column(db.ForeignKey('person.id'))
    person = db.relationship("Person", back_populates="last_seen")

    def __init__(self, latitude, longitude, existent=False):
        self.existent = existent
        self.latitude = latitude if existent else None
        self.longitude = longitude if existent else None

    def __repr__(self):
        return '<Location - id {}>'.format(self.id)

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'existent': self.existent
        }
