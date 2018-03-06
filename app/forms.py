from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import DataRequired, Optional

class signup_form(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    cancer_type = StringField('cancer_type', validators=[DataRequired()])

class login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('password', validators=[DataRequired()])

class personal_information(FlaskForm):
    dob = StringField('date_of_birth', validators=[DataRequired()])
    current_location = StringField('location', validators=[DataRequired()])
    ethnicity = StringField('ethnicity', validators=[DataRequired()])
    income = IntegerField('income', validators=[Optional()])

class cancer_information(FlaskForm):
    cancer_type = RadioField('cancer_type', choices=[('1', 'Breast Cancer'),('2', 'Other')], validators=[DataRequired()])
    diagnosis_date_year = IntegerField('diagnosis_date', validators=[DataRequired()])
    cancer_stage = RadioField('cancer_stage', choices=[('1', 'Stage 1'), ('2', 'Stage 2'), ('3', 'Stage 3'), ('4', 'Other')], validators=[DataRequired()])

class cancer_metastasis(FlaskForm):
    metastatis_boolean = RadioField('metastatis_boolean', choices=[('1', 'yes'),('2', 'no')], validators=[DataRequired()])
    # metastasis_site = SelectMultipleField('Sites of Metastasis', choices=[('liver', 'Liver'), ('esophogus', 'Esophogus'), ('liver', 'Liver')])
    metastasis_diagnosis_date_year = IntegerField('metastasis_diagnosis_date', validators=[DataRequired()])
    stage = IntegerField('stage', validators=[DataRequired()])
