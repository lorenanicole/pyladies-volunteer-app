##Overview
![Imgur](http://i.imgur.com/TddsutV.png =300x)

The PyLadies Chicago Volunteer App is a Flask app using (Flask-SQLAlchemy extension) SQLAlchemy ORM.

###Environment Setup

Create a virtualenv and use the requirements.txt to install the project libraries:

```
virtualenv pyladies-env
source pyladies-env/bin/activate
cd pyladies-volunteer-app
pip install -r requirements.txt
```

This app was written with the latest flavor of Flask, 0.11dev. To acquire this version you can follow the [Living on the Edge](http://flask.readthedocs.org/en/latest/installation/#installation) instructions. Please note that <b>pip</b> does not have the development version code available.

You'll need to have your virtualenv use the latest code on the Git repo:

```
git clone http://github.com/mitsuhiko/flask.git
virtualenv pyladies-env
cd flask
python setup.py develop
# Watch the magic happen
``` 

###To Run Locally

```
cd pyladies-volunteer-app
python run.py
```

Flask app will be accessible at http://localhost:5000/

###APIs & Config
PyLadies events information is created and updated by calling the [MeetUp API](http://www.meetup.com/meetup_api/), you'll need to store an [API key](https://secure.meetup.com/meetup_api/key/) in a config file. 

The email service, powered by [Flask-Mail extension](https://pythonhosted.org/Flask-Mail/), will require login credentials  to be added the config file. Miguel Grinberg wrote an [excellent blog post](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support) discussing how to setup email config.