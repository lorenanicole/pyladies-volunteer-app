##Overview
![Imgur](http://i.imgur.com/TddsutV.png =300x)

The PyLadies Chicago Volunteer App is a Flask 0.10 app using (Flask-SQLAlchemy extension) SQLAlchemy ORM.

###Environment Setup

Create a virtualenv and use the requirements.txt to install the project libraries:

```
virtualenv pyladies-env
source pyladies-env/bin/activate
cd pyladies-volunteer-app
pip install -r requirements.txt
```

###To Run Locally

```
cd pyladies-volunteer-app
python run.py
```

Flask app will be accessible at http://localhost:5000/

###APIs & Config
PyLadies events information is created and updated by calling the [MeetUp API](http://www.meetup.com/meetup_api/), you'll need to store an [API key](https://secure.meetup.com/meetup_api/key/) in a config file (e.g. config.py).

The email service, powered by [Flask-Mail extension](https://pythonhosted.org/Flask-Mail/), will require login credentials  to be added the config file. Miguel Grinberg wrote an [excellent blog post](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support) discussing how to setup email config.