from flask import Flask, current_app, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import app.forms as forms
# import signup_form, login_form
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import pytz
import app.config as config

logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__)

application.config.from_object(config)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
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


@application.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(request.json)
        return 'Thanks for returning!'
    if request.method == 'GET':
        return current_app.send_static_file('index.html')


@application.route('/signup', methods=('GET', 'POST'))
def submit():
    print("on submit page")
    form = forms.signup_form()
    if form.validate_on_submit():
        print(form.email.data)
        print("submitted!")
        new_user = User_Info(form.email.data, form.password.data, form.username.data, form.first_name.data, form.last_name.data, form.cancer_type.data)
        db.session.add(new_user)
        db.session.commit()
        # return redirect('/success')
    return render_template('signup_form.html', form=form)


# @application.route('/signed_in')
# def submit():
#     return "Successfully created account! Yay!"

@application.route('/personal', methods=('GET', 'POST'))
def submit():
    form = forms.personal_information()
    if form.validate_on_submit():
        print(form.email.data)
        print("submitted!")
        new_user = User_Info(form.email.data, form.password.data, form.username.data, form.first_name.data, form.last_name.data, form.cancer_type.data)
        db.session.add(new_user)
        db.session.commit()
        # return redirect('/success')
    return render_template('signup_form.html', form=form)
