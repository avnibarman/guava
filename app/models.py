from .app import db
from sqlalchemy.dialects.postgresql import JSON
import pytz
import datetime.datetime


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