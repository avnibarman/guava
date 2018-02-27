from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

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
