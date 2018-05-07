# CancerBase Lifestory
CancerBase Lifestory is a journaling application for cancer patients. For full context on the aapplication's design and purpose, refer to the pdf.

The application is built using [Flask, a python microframework](http://flask.pocoo.org/).

This repo contains code for a prototype of the app with only partial functionality. The experience of the app is what the final app should be, but currently it does not save data to a persistent database. The comments in the code detail the specifics of how data is stored for now.

## Running the code

The application uses [pipenv](https://docs.pipenv.org/) as a package manager and virtual environment. Once you have pipenv installed, you can run:
`pipenv install`
to install the necessary dependencies.

Next, enter the pipenv shell by running:
`pipenv shell`

Now you can run the code. Simply run
`python application.py`
and the app will run on localhost. 

Then you can navigate to `localhost:5000` and view the app.


## Summary of codebase

### application.py
This file just starts the flask application.

### manage.py
This file is deprecated but included for reference in case it's helpful to see how we handled the database.

### migrations folder
This folder is used by [SQLalchemy](https://www.sqlalchemy.org/), and shouldn't need to be edited. It may need to be deleted if the SQLalchemy or database configuration changes.

### .elasticbeanstalk, .ebextensions
These folders were used for deploying to AWS's elastic beanstalk service. They can be ignored or deleted unless you want to use them later to deploy to elastic beanstalk.

### app folder
This folder contains the codebase for the application.

### app/templates
This folder contains the Jinja2 templates that are rendered into HTML for the user to view. Any changes to the frontend interface may involve changing these templates.

### app/static
This folder contains static files served by the app, including css files and images.

### app/__init__.py
This file contains the majority of the code for the application. It serves routes and contains much of the logic.

### app/config.py
This file contains various configuration settings for the app.

### app/forms.py
This file creates forms using [WTForms for Flask](https://flask-wtf.readthedocs.io/en/stable/). We used WTForms for our example login flow in the demo, but the flow is separate from the rest of the application so this file is not important for the prototype.

### application/manage.py
This file was used to manage the database using SQLAlchemy, and may be useful for reference but can otherwise be ignored.
