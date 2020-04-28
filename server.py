import os
import datetime
from flask import Flask, jsonify, render_template, url_for, g, redirect, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from tronald import tronald_dumps
from flask_migrate import Migrate
from mapbox import Geocoder
import flight_service
import weather_service

app = Flask(__name__)
target_port = 3000
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'wman.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'castelldefels'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
location = ''
destination = 'Malaga'


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    address = StringField('What is your address?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    latitude = db.Column(db.String(64), unique=True, index=True)
    longitude = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, latitude, longitude):
        self.username = username
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<User %r>' % self.username



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

# to get around browser caching of css...
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

# **values param represents the variables for the URL...


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


@app.route('/', methods=['GET', 'POST'])
def home():
    mapbox_access_token = 'pk.eyJ1IjoibWF0dG9mZmljZSIsImEiOiJjazlqdHYwZ2kwMHBxM2xscmF5bzdpc2dsIn0.iDUw71WZCer5ZrbOkEusqg'
    name = None
    address = 'Algernon Terrace'
    coords = [-1.435385, 55.019037]
    location = ''
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        location = form.address.data
        geocoder = Geocoder(
            access_token="pk.eyJ1IjoibWF0dG9mZmljZSIsImEiOiJjazlqdHYwZ2kwMHBxM2xscmF5bzdpc2dsIn0.iDUw71WZCer5ZrbOkEusqg")
        coords = geocoder.forward(address).json()[
            'features'][0]['geometry']['coordinates']
    return render_template('home.html', form=form, name=name, address=address, coords=coords, mapbox_access_token=mapbox_access_token, location=location)


@app.route('/flights/<destination>', methods=['GET'])
def serve_flights(destination):
    destination = destination
    fs = flight_service.Flight_Service(destination, '2020-08-01')
    res = fs.call_amadeus()
    #destination = request.args.get('destination', type=str)
    # print(destination)
    return render_template('flights.html', flight_data=fs.data, destination=destination)


@app.route('/weather/<destination>', methods=['GET'])
def serve_weather(destination):
    destination = destination
    ws = weather_service.Weather_Service(destination)
    w_data = ws.call_weather_api()
    return render_template('weather.html', weather_data=w_data, destination=destination)


@app.route('/map', methods=['GET', 'POST'])
def my_maps():

    mapbox_access_token = 'pk.eyJ1IjoibWF0dG9mZmljZSIsImEiOiJjazlqdHYwZ2kwMHBxM2xscmF5bzdpc2dsIn0.iDUw71WZCer5ZrbOkEusqg'

    return render_template('map.html',
                           mapbox_access_token=mapbox_access_token)


if __name__ == '__main__':
    app.run(host="localhost", port=target_port)
