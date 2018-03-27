from flask import Flask, current_app, request, render_template, redirect
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
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_user, current_user


logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__)

application.config.from_object(config)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class User(UserMixin):
    def __init__(self, id, username, first_name):
        self.id = id
        self.username = username
        self.first_name = first_name
    
    @property
    def is_active(self):
        return True
    @property
    def is_authenticated(self):
        return True
    @property
    def is_anonymous(self):
        return False



login_manager = LoginManager()
login_manager.init_app(application)
@login_manager.user_loader
def load_user(user_id):
    account = db.session.query(User_Info).filter_by(user_id=user_id).first()
    user = User(account.user_id, account.username, account.first_name)
    return user


class User_Info(db.Model):
    __tablename__ = 'accounts'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(355), unique=True, nullable=False)
    password = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.TIMESTAMP)
    last_login = db.Column(db.TIMESTAMP)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cancer_type = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password, username, first_name, last_name, cancer_type):
        self.email = email
        self.password = sha256_crypt.encrypt(password)
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.cancer_type = cancer_type
        now = datetime.now()
        pst = pytz.timezone('America/Los_Angeles')
        self.created_on = pst.localize(now)
        self.last_login = None

    def __repr__(self):
        return '<id {}>'.format(self.user_id)


class Personal_Information(db.Model):
    __tablename__ = 'personal_info'

    user_id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Integer, nullable=False)
    current_location = db.Column(db.String(255))
    ethnicity = db.Column(db.String(50), nullable=True)
    income = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.TIMESTAMP)

    def __init__(self, dob, current_location, ethnicity, income):
        self.dob = dob
        self.current_location = current_location
        self.ethnicity = ethnicity
        self.income = income

    def __repr__(self):
        return '<id {}>'.format(self.user_id)


class Cancer_Information(db.Model):
    __tablename__ = 'cancer_info'

    user_id = db.Column(db.Integer, primary_key=True)
    cancer_type = db.Column(db.String(50), nullable=False)
    diagnosis_date_year = db.Column(db.String(4))
    cancer_stage = db.Column(db.Integer, nullable=True)

    def __init__(self, cancer_type, diagnosis_date_year, cancer_stage):
        self.cancer_type = cancer_type
        self.diagnosis_date_year = diagnosis_date_year
        self.cancer_stage = cancer_stage

    def __repr__(self):
        return '<id {}>'.format(self.user_id)


class Metastasis_Information(db.Model):
    __tablename__ = 'metastasis_info'

    user_id = db.Column(db.Integer, primary_key=True)
    metastasis_site_1 = db.Column(db.String(50), nullable=True)
    metastasis_diagnosis_date_year_1 = db.Column(db.String(4))
    metastasis_site_2 = db.Column(db.String(50), nullable=True)
    metastasis_diagnosis_date_year_2 = db.Column(db.String(4))
    metastasis_site_3 = db.Column(db.String(50), nullable=True)
    metastasis_diagnosis_date_year_3 = db.Column(db.String(4))
    metastasis_site_4 = db.Column(db.String(50), nullable=True)
    metastasis_diagnosis_date_year_4 = db.Column(db.String(4))

    def __init__(self, metastasis_site_1, metastasis_diagnosis_date_year_1, 
        metastasis_site_2, metastasis_diagnosis_date_year_2,
        metastasis_site_3, metastasis_diagnosis_date_year_3,
        metastasis_site_4, metastasis_diagnosis_date_year_4):
        self.metastasis_site_1 = metastasis_site_1
        self.metastasis_diagnosis_date_year_1 = metastasis_diagnosis_date_year_1
        self.metastasis_site_2 = metastasis_site_2
        self.metastasis_diagnosis_date_year_2 = metastasis_diagnosis_date_year_2
        self.metastasis_site_3 = metastasis_site_3
        self.metastasis_diagnosis_date_year_3 = metastasis_diagnosis_date_year_3
        self.metastasis_site_4 = metastasis_site_4
        self.metastasis_diagnosis_date_year_4 = metastasis_diagnosis_date_year_4

    def __repr__(self):
        return '<id {}>'.format(self.user_id)


class Daily_Log(db.Model):
    __tablename__ = 'daily_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    subjective_wellbeing = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    appetite = db.Column(db.Integer)
    dizziness = db.Column(db.Integer)
    pain = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    journal = db.Column(db.String(1000), nullable=True)

    def __init__(self, 
        user_id, 
        subjective_wellbeing, 
        energy, 
        appetite,
        dizziness, 
        pain,
        strength, 
        journal):
        self.subjective_wellbeing = subjective_wellbeing
        self.energy = energy
        self.appetite = appetite
        self.dizziness = dizziness
        self.pain = pain
        self.strength = strength
        self.journal = journal
    
    def __repr__(self):
        return '<id {}>'.format(self.log_id)


@application.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(request.json)
        return 'Thanks for returning!'
    if request.method == 'GET':
        return current_app.send_static_file('index.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.login_form()
    if form.validate_on_submit():
        user_info = db.session.query(User_Info).filter_by(username=form.username.data).first()
        user_id = user_info.user_id
        user_object = load_user(user_id)
        print("password: ", user_info.password)
        if sha256_crypt.verify(form.password.data, user_info.password):
            # yay they put in the right password
            login_user(user_object)
            print("Current User: ", current_user)
            print("username: ", current_user.username)
            print("id:", current_user.id)
            return redirect('/daily_checkin')
        else:
            print("Incorrect login attempt.")
            return 'Login incorrect. Please return to the login page and try again.'
    else:
        return render_template('login_form.html', form=form)


@application.route('/daily_checkin', methods=['GET', 'POST'])
def daily_checkin():
    today_formatted = "Tuesday March 27, 2018"
    form = forms.daily_checkin()
    print("current id: ", current_user.id)
    if form.validate_on_submit():
        print("form validated")
        new_log = Daily_Log(
            current_user.id,
            form.subjective_wellbeing.data, 
            form.energy.data, 
            form.appetite.data, 
            form.dizziness.data, 
            form.pain.data, 
            form.strength.data,
            form.journal.data
        )
        db.session.add(new_log)
        db.session.commit()
        return redirect('thanks')
    else:
        return render_template(
            'daily_checkin.html', 
            today_formatted=today_formatted,
            form=form
        )

@application.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

@application.route('/signup', methods=('GET', 'POST'))
def signup():
    form = forms.signup_form()
    if form.validate_on_submit():
        new_user = User_Info(form.email.data, form.password.data, form.username.data, form.first_name.data, form.last_name.data, form.cancer_type.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/personal_information')
    else:
        return render_template('signup_form.html', form=form)


@application.route('/personal_information', methods=('GET', 'POST'))
def personal_information():
    form = forms.personal_information()
    if form.validate_on_submit():
        user_info = Personal_Information(form.dob.data, form.current_location.data, form.ethnicity.data, form.income.data)
        db.session.add(user_info)
        db.session.commit()
        return redirect('/cancer_information')
    else:
        return render_template('personal_information.html', form=form)


@application.route('/cancer_information', methods=('GET', 'POST'))
def cancer_information():
    form = forms.cancer_information()
    if form.validate_on_submit():
        cancer_info = Cancer_Information(form.cancer_type.data, form.diagnosis_date_year.data, form.cancer_stage.data)
        db.session.add(cancer_info)
        db.session.commit()
        return redirect('/metastasis_information')
    else:
        return render_template('cancer_information.html', form=form)


@application.route('/metastasis_information', methods=('GET', 'POST'))
def metastasis_information():
    form = forms.metastasis_information()
    if form.validate_on_submit():
        metastasis_info = Metastasis_Information(
            form.metastasis_site_1.data, 
            form.metastasis_diagnosis_date_year_1.data, 
            form.metastasis_site_2.data,
            form.metastasis_diagnosis_date_year_2.data, 
            form.metastasis_site_3.data,
            form.metastasis_diagnosis_date_year_3.data, 
            form.metastasis_site_4.data,
            form.metastasis_diagnosis_date_year_4.data
        )
        db.session.add(metastasis_info)
        db.session.commit()
        return redirect('/login')
    return render_template('metastasis_information.html', form=form)
