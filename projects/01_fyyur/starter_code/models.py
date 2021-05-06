#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
db = SQLAlchemy()

class Show(db.Model):
    __tablename__ = 'shows'

    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    start_time = db.Column('start_time', db.DateTime, primary_key=True)
    def __repr__(self):
        return f'<Show {self.venue_id} {self.artist_id} >'


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default =False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="venue", cascade = "all,delete" , lazy=True)
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.genres} {self.website_link} >'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default =False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="artist", cascade = "all,delete", lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.website_link} {self.facebook_link} {self.seeking_venue} {self.seeking_description} {self.shows}>'
