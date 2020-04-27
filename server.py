import os
import datetime
from flask import Flask, jsonify, render_template, url_for, g, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from tronald import tronald_dumps
from flask_migrate import Migrate
import flight_service
import weather_service

app = Flask(__name__)
target_port = 3000
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'wman.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
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
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, latitude, longitude):
        self.username = username
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<User %r>' % self.username


fs = flight_service.Flight_Service('Madrid', '2020-08-01')
res = fs.call_amadeus()
ws = weather_service.Weather_Service('Madrid')
w_data = ws.call_weather_api()
print(res)


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
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data,
                        latitude=float(55.0176), longitude=float(4.764))
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('home'))
    return render_template('home.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/flights', methods=['GET'])
def serve_flights():
    return render_template('flights.html', flight_data=fs.data, random_list=[4, 5, 6, 7, 8, 9])


@app.route('/weather', methods=['GET'])
def serve_weather():
    return render_template('weather.html', weather_data=w_data)


if __name__ == '__main__':
    app.run(host="localhost", port=target_port)
