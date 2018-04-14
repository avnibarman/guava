
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
# from flask_login import LoginManager, UserMixin, login_user, current_user


logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__)

application.config.from_object(config)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

# class User(UserMixin):
#     def __init__(self, id, username, first_name):
#         self.id = id
#         self.username = username
#         self.first_name = first_name
    
#     @property
#     def is_active(self):
#         return True
#     @property
#     def is_authenticated(self):
#         return True
#     @property
#     def is_anonymous(self):
#         return False



# login_manager = LoginManager()
# login_manager.init_app(application)
# @login_manager.user_loader
# def load_user(user_id):
#     account = db.session.query(User_Info).filter_by(user_id=user_id).first()
#     user = User(account.user_id, account.username, account.first_name)
#     return user


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
        # user_info = db.session.query(User_Info).filter_by(username=form.username.data).first()
        # user_id = user_info.user_id
        # user_object = load_user(user_id)
        # print("password: ", user_info.password)
        # if sha256_crypt.verify(form.password.data, user_info.password):
        #     # yay they put in the right password
        #     # login_user(user_object)
        #     print("Current User: ", current_user)
        #     print("username: ", current_user.username)
        #     print("id:", current_user.id)
        return redirect('/daily_checkin')
        # else:
        #     print("Incorrect login attempt.")
        #     return 'Login incorrect. Please return to the login page and try again.'
    else:
        return render_template('login_form.html', form=form)


@application.route('/daily_checkin', methods=['GET', 'POST'])
def daily_checkin():
    today_formatted = "Tuesday March 27, 2018"
    form = forms.daily_checkin()
    current_user = {}
    # current_user["name"] = "Landon"
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
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
            form=form,
            current_user=current_user
        )

memoirs = [
  {
        "type": "entry",
        "title": "Wedding Day",
        "chapter": "Early Adulthood",
        "body": """
          Oh my goodness, my wedding day. Well first a little backstory.
          <br>
          My parents were very much against my wedding to Noah, so my wedding day, it was a small thing.
          <br>
          It’s funny because in some ways I felt like it was done mostly for my parents, in some sense, but also against them as well.
          <br>
          It was all kind of everyday. I remember shopping in the mall for a white dress that I could wear for my wedding day and then going and getting my hair braided up pretty. My friend Kimberly arranged the bouquet, which was sweet, but I had already chosen the flowers I wanted because they symbolize the different women in my family to me. 
          <br>
          Hmm, who was there? Sara Williams, my childhood friend, came. And John Miller. And Kimberly and her boyfriend at the time, Brandon. Noah’s mentor from Israel was there, Moshe. And a friend of Noah’s from grad school, Paul. And then Angela, my friend from grad school came – she’s the one who took all the pictures that appear in my album. And Yael and Eric Simmons came too, because Yael was a friend of Noah’s. And Gary Stone was there, Gary was a colleague of Noah’s at the time. Oh and Mom and Dad came, they reluctantly showed up and it was awkward... it was ok, that was it. 
          <br>
          And then we got to move into Married Student Housing! Because we couldn’t possibly live in Married Student Housing before that, that was impossible back then – It was for married people only, not just people living together. That was one of the motivators in the whole thing.
          <br>
          There was no particular honeymoon. We tried driving up to Maine – I wanted to go see the Bay of Fundy, where there’s a big permanent whirlpool. We made it to Bar Harbor, Maine and Noah was so—I don’t know—unhappy with the notion of taking a vacation that we had to turn back. So we never quite had that honeymoon. "
        """
    },

    {
        "type": "entry",
        "title": "Childhood Neighborhood",
        "chapter": "Childhood",
        "body": """
          I lived in a suburb of Chicago—a far western suburb so not all that close to Chicago—called Elmhurst, Illinois. I lived on a block, in a split-level house that sat on a quarter acre. I would walk to elementary school which was a few blocks away, or down the block to pick up the school bus that would take us to high school later on. It was the kind of neighborhood where you look down the street and you knew who the neighbors were. The kids would all get together to play after school or during summer vacation. Our house had a backyard and a front yard and you could walk to most places from it; the nearest strip mall was a little under a mile away.
          <br>
          It was very much the suburbia that is characteristic of the Midwest; there were no fences.
          <br>
          Well, I remember when our neighbors put up fences around their backyard and how there was some jockeying about where a fence goes and in whose property line and stupid things like that—but I guess that’s still present today.
          Eventually it all got fenced off.
          <br>
          My mom was one of the only moms that worked. And she sometimes got frustrated because all the other moms would go “Oh, you’re missing out on the best years of your kids’ lives!” and she would say back to them “Whatever! You have no clue!” We had a sitter instead, Augusta, who was black, and that was very unusual for our town. Our town was homogenous, very white.
        """
    },

    {
        "type": "entry",
        "title": "Bad Weather Adventures",
        "chapter": "Teen Years",
        "body": """
          I went to a summer camp that really shaped my life for 4 years in Bloomington, Indiana.
          <br>
          At the beginning of every summer, there was a staff week where we’d all get together before camp started. That week the Counselors in Training (CIT’s) would get trained, and old counselors would share wisdom. For the week, the staffs gets split into different speciality teams—there was caving, canoeing, hiking, belaying, etc. etc. 
          <br>
          I was a hiking specialty my first year. It was my very first hike as a CIT. The sun was setting, it was a gorgeous sunset, with beautiful, full clouds. About an hour later it started pouring. The forecast did not call for rain, we didn’t have anything prepared. 
          <br>
          Our backpacks were drenched, our tents were drenched, WE were drenched. It was raining so hard that there was a flash flood warning and the trail got washed away! We completely lost track of the trail and our direction. We were supposed to be following an easy, relaxing 12 mile hike, but because of the rain it turned into 30 miles of slogging through mud. We didn’t have any phones or other means of contact to get help, so we had to rely on metal compasses to find our way through the forest.
          <br>
          It took us three days to get back to base camp. 
        """
    }
]

def search_memoirs(key, value):
    ret = []
    for memoir in memoirs:
        if memoir[key] == value:
            ret.append(memoir)
    return ret


@application.route('/view_memoirs/<entry_title>', methods=['GET', 'POST'])
def view_memoirs(entry_title):
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    memoir = search_memoirs("title", entry_title)[0]

    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir,
        memoir_chapter=memoir['chapter']
    )


@application.route('/enter', methods=['GET', 'POST'])
def enter_memoirs():
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    memoir = {
        "type": "portal"
    }
    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir
    )


@application.route('/memoir_entry', methods=['GET', 'POST'])
def memoir_entry():
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    memoir = {
        "type": "entry",
        "title": "Memorable Road Trip",
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
    memoir_chapter = "childhood"
    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir,
        memoir_chapter=memoir_chapter
    )


@application.route('/memoir_table_of_contents', methods=['GET', 'POST'])
def memoir_table_of_contents():
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    memoir = {
        "type": "directory",
        "title": "Table of Contents",
        "sections": [
            {"title": "Childhood"},
            {"title": "Teen Years"},
            {"title": "Early Adulthood"},
            {"title": "Late Adulthood"}
        ]
    }
    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir,
        backlink="/enter"
    )

@application.route('/memoir_table_of_contents/<chapter>', methods=['GET', 'POST'])
def table_of_contents(chapter):
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    # sections = /
    memoir = {
        "type": "directory",
        "title": chapter,
        "sections": search_memoirs("chapter", chapter)
    }
    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir,
        backlink="/memoir_table_of_contents"
    )

@application.route('/view_all_memories', methods=['GET', 'POST'])
def view_all_memories():
    current_user = {}
    current_user["first_name"] = "Landon"
    current_user["id"] = 0
    # leaving these just so I know the schemas!
    memories = memoirs
    return render_template(
        'view_all_memories.html',
        current_user=current_user,
        memories=memories
    )

@application.route('/submit_memory', methods=['GET', 'POST'])
def submit_memory():
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0
    memoir = {"title": "Reflect on a time when you felt proud."}
    return render_template(
        'submit_memory.html',
        current_user=current_user,
        memoir=memoir
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
