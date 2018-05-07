
from flask import Flask, current_app, request, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import app.forms as forms
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import pytz
import app.config as config
from passlib.hash import sha256_crypt


logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__)

application.config.from_object(config)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


@application.route('/', methods=['GET'])
def hello_world():
    """
    This route simply returns a static index page. 
    This could be used as a landing page or portal to the app.
    """
    if request.method == 'GET':
        return current_app.send_static_file('index.html')

# the memoirs list should be pulled from a database.
# For now, it's simply created statically.

# A memoir entry is a dictionary with the following fields:
# type: a string that is "entry",
# title: a string representing the title of the entry, as set by a user.
# chapter: a string that is one of 
#       ("Childhood", "Teen Years", "Early Adulthood", or "Later Adulthood")
# body: a string that represents the HTML to be placed inside the paragraph on an entry

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
    """
    This is a simple helper function to find a list of items that 
    match search criteria in the memoirs list.
    
    arguments:
    key -- the key of the memoir entry to consider
    value -- the value of the memoir entry to search for

    returns:
    a list of memoirs that have the specified key value pair in them.
    if none match the criteria, it returns an empty list.
    """
    ret = []
    for memoir in memoirs:
        if memoir[key] == value:
            ret.append(memoir)
    return ret


@application.route('/view_memoirs/<entry_title>', methods=['GET', 'POST'])
def view_memoirs(entry_title):
    """
    This route is for viewing a specific memoir in the memoir object.

    arguments:
    entry_title -- the title of the entry to show.
    """
    # current_user should actually be dealt with using some session management library pulling from database.
    # for now it's just static
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
    """
    This is the first page someone should see when using the Horizon app.
    It's just a simple portal to the experience.
    """
    # again, current_user is an object that should be pulled from the session after someone logs in.
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0

    # since this is using the view_memoirs template, you must include a memoir object.
    # give it "type": "portal" to have the template render the correct page.
    memoir = {
        "type": "portal"
    }
    return render_template(
        'view_memoirs.html',
        current_user=current_user,
        memoir=memoir
    )


@application.route('/memoir_table_of_contents', methods=['GET', 'POST'])
def memoir_table_of_contents():
    """
    After clicking the "enter" button on the "/enter" route, the user is taken to 
    the table of contents.

    The root page of the table of contents simply lists the four sections of
    the memoir that we've defined: Childhood, Teen years, Early Adulthood, and
    Late Adulthood.
    """
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0

    # since this route uses the view_memoirs template, it expects a memoir dictionary.
    # for table of contents pages, it uses a dictionary with "type": "directory" as
    # one of the key value pairs. The other fields it expects are:
    # "title": A string- The title for this "page" of the "book".
    # "sections": A list of dicts of the form {"title": string} where each section is a link
    # to another page.
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
    """
    This is another table of contents page that shows the contents of a specific life chapter.

    arguments:
    chapter -- the name of the chapter to view the contents of.
            should be one of ("Childhood", "Teen Years", "Early Adulthood", or "Later Adulthood")
    """
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0

    # same as the memoir_table_of_contents route, it uses a dictionary of type "directory"
    # it dynamically gets the chapters from the memoir list using the search_memoirs function
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
    """
    This is a page for viewing and searching through all the memoirs that have been created.
    """
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0

    # uses full memoirs list
    memories = memoirs
    return render_template(
        'view_all_memories.html',
        current_user=current_user,
        memories=memories
    )

@application.route('/submit_memory', methods=['GET', 'POST'])
def submit_memory():
    """
    This is a page for writing new memories.
    Currently it doesn't save the memoir anywhere, but in the future
    it should post it to a database.
    """
    current_user = {}
    current_user["first_name"] = "Barbara"
    current_user["id"] = 0

    return render_template(
        'submit_memory.html',
        current_user=current_user
    )
