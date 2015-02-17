import datetime
import pytz
from sqlalchemy import PrimaryKeyConstraint
import settings

__author__ = 'lorenamesa'

import os
from flask import Flask, g
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.path.join(app.root_path, 'pyladies.db')
db = SQLAlchemy(app)


app.secret_key = 'SuperSecretThings'
app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
app.config['ADMINS'] = settings.ADMINS

app.config.from_object(__name__) # adds config setting
mail = Mail(app)

# @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     print('Initialized the database.')

## CONTENT PROCESSOR

@app.context_processor
def date_processor():
    def get_human_readable_date(time):
        '''
        :param time: is an epoch time string length 10
        '''
        naive = datetime.datetime.utcfromtimestamp(time)
        tz = pytz.timezone("America/Chicago")
        tzoffset = tz.utcoffset(naive)
        localized = tzoffset + naive
        return localized.strftime('%Y-%m-%d %I:%M')


    return dict(get_human_readable_date=get_human_readable_date)

@app.context_processor
def time_processor():
    def get_num_of_hours(time_in_milliseconds):
        '''
        :param time_in_milliseconds: as it sounds :-)
        :return: num_of_hours (3600000 ms per hour)
        '''
        return time_in_milliseconds / 3600000
    return dict(get_num_of_hours=get_num_of_hours)

from app import views