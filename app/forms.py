from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import IntegerRangeField


class signup_form(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    cancer_type = StringField('cancer_type', validators=[DataRequired()])


class login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class personal_information(FlaskForm):
    dob = StringField('date_of_birth', validators=[DataRequired()])
    current_location = StringField('location', validators=[DataRequired()])
    ethnicity = StringField('ethnicity', validators=[DataRequired()])
    income = IntegerField('income', validators=[Optional()])


class cancer_information(FlaskForm):
    cancer_type = StringField('date_of_birth', validators=[DataRequired()])
    diagnosis_date_year = IntegerField('diagnosis_date', validators=[DataRequired()])
    cancer_stage = SelectField('cancer_stage', choices=[('1', 'Stage 1'), ('2', 'Stage 2'), ('3', 'Stage 3'), ('4', 'Other')], validators=[DataRequired()])


class metastasis_information(FlaskForm):
    metastasis_site_choices = [
        ('none', 'None'),
        ('breast', 'Breast'), 
        ('bone', 'Bone'), 
        ('chest_wall', 'Chest Wall'),
        ('lung', 'Lung'),
        ('lymph_node', 'Lymph Node'),
        ('liver', 'Liver'),
        ('brain', 'Brain'),
        ('contra_breast', 'Contralateral Breast'),
        ('ab_wall', 'Ab Wall'),
        ('skin', 'Skin'),
        ('ovary', 'Ovary'),
        ('adrenal', 'Adrenal'),
        ('intestine', 'Intestine'),
        ('kidney', 'Kidney'),
        ('bladder', 'Bladder'),
        ('cervix', 'Cervix'),
        ('thyroid', 'Thyroid'),
        ('eye', 'Eye'),
        ('pancreas', 'Pancreas'),
        ('muscles', 'Muscles'),
        ('spleen', 'Spleen'),
        ('uterus', 'Uterus'),
        ('stomach', 'Stomach'),
        ('pericardium', 'Pericardium'),
        ('parotid', 'Parotid'),
        ('pharynx', 'Pharynx'),
        ('vagina', 'Vagina'),
        ('gallbladder', 'Gallbladder'),
        ('aorta', 'Aorta'),
        ('other', 'Other')
    ]
    metastasis_site_1 = SelectField('Site of First Metastasis', choices=metastasis_site_choices)
    metastasis_diagnosis_date_year_1 = IntegerField('Date of Metastasis', validators=[Optional()])
    metastasis_site_2 = SelectField('Site of Second Metastasis', choices=metastasis_site_choices)
    metastasis_diagnosis_date_year_2 = IntegerField('Date of Metastasis', validators=[Optional()])
    metastasis_site_3 = SelectField('Site of Third Metastasis', choices=metastasis_site_choices)
    metastasis_diagnosis_date_year_3 = IntegerField('Date of Metastasis', validators=[Optional()])
    metastasis_site_4 = SelectField('Site of Fourth Metastasis', choices=metastasis_site_choices)
    metastasis_diagnosis_date_year_4 = IntegerField('Date of Metastasis', validators=[Optional()])


class daily_checkin(FlaskForm):
    face_choices = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]
    subjective_wellbeing = RadioField('faces', choices=face_choices, validators=[Optional()])
    energy = IntegerRangeField('Energy', default=3, validators=[Optional()])
    appetite = IntegerRangeField('Appetite', default=3, validators=[Optional()])
    dizziness = IntegerRangeField('Dizziness', default=3, validators=[Optional()])
    pain = IntegerRangeField('Pain', default=3, validators=[Optional()])
    strength = IntegerRangeField('Strength', default=3, validators=[Optional()])
    energy = IntegerRangeField('Energy', default=3, validators=[Optional()])
    journal = TextAreaField('journal', validators=[Optional()])
