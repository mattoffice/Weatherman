import os
import datetime
from flask import Flask, jsonify, render_template, url_for, g, redirect, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
#from tronald import tronald_dumps
from mapbox import Geocoder
import flight_service
import weather_service

app = Flask(__name__)
target_port = 3000
bootstrap = Bootstrap(app)

DB_URL = 'postgresql+psycopg2://postgres:Castelldefels@34.76.239.106/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rosario'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


location = ''
destination = 'Malaga'


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    current_location = StringField('Where are you now?',
                                   validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    currentLocation = db.Column(db.String(120), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, username, currentLocation):
        self.username = username
        self.currentLocation = currentLocation

    def __repr__(self):
        return '<User %r>' % self.username


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
    current_location = 'Algernon Terrace'
    coords = [-1.435385, 55.019037]
    location = ''
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        name = form.name.data
        current_location = form.current_location.data
        geocoder = Geocoder(
            access_token="pk.eyJ1IjoibWF0dG9mZmljZSIsImEiOiJjazlqdHYwZ2kwMHBxM2xscmF5bzdpc2dsIn0.iDUw71WZCer5ZrbOkEusqg")
        coords = geocoder.forward(current_location).json()[
            'features'][0]['geometry']['coordinates']
        if user is None:
            user = User(username=form.name.data,
                        currentLocation=current_location)
            db.session.add(user)

            db.session.commit()
        session['name'] = name
        session['current_location'] = current_location
        form.name.data = ''
        form.current_location.data = ''
    return render_template('home.html', form=form, name=session.get('name'), current_location=session.get('current_location'), coords=coords, mapbox_access_token=mapbox_access_token)


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
