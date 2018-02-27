from flask import Flask, current_app, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from .forms import signup_form, login_form
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import pytz

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
secret_key = ""
with open ("aws-key.pem", "r") as myfile:
    secret_key = myfile.read()
Config = {
    'DEBUG': True,
    'TESTING': False,
    'CSRF_ENABLED': True,
    'SECRET_KEY': secret_key,
    'WTF_CSRF_SECRET_KEY': 'a csrf secret key',
    'SQLALCHEMY_DATABASE_URI': 'postgresql://dre:disruption@cbdb.cjvamjemslrm.us-west-1.rds.amazonaws.com:5432/cbdb'
}

app.config.update(dict(
    SECRET_KEY=secret_key,
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='postgresql://dre:disruption@cbdb.cjvamjemslrm.us-west-1.rds.amazonaws.com:5432/cbdb',
    DEBUG=True
))

app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
print("hello world!")



class User_Info(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(355), unique=True, nullable=False)
    password = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.TIMESTAMP)
    last_login = db.Column(db.TIMESTAMP)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cancer_type = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password, username, first_name, last_name, cancer_type):
        self.email = email
        self.password = password
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.cancer_type = cancer_type
        now = datetime.now()
        pst = pytz.timezone('America/Los_Angeles')
        self.created_on = pst.localize(now)
        self.last_login = None

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(request.json)
        return 'Thanks for returning!'
    if request.method == 'GET':
        return current_app.send_static_file('index.html')


@app.route('/signup', methods=('GET', 'POST'))
def submit():
    print("on submit page")
    form = signup_form()
    if form.validate_on_submit():
        print(form.email.data)
        print("submitted!")
        new_user = User_Info(form.email, form.password, form.username, form.first_name, form.last_name, form.cancer_type)
        db.session.add(new_user)
        db.session.commit()
        # return redirect('/success')
    return render_template('signup_form.html', form=form)


# @app.route('/signed_in')
# def submit():
#     return "Successfully created account! Yay!"
