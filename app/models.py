import urllib
from itsdangerous import Serializer
from sqlalchemy import PrimaryKeyConstraint, text
from app import db, app
from app.emails import send_email
from app.helpers import get_human_readable_date
from app.settings import ADMINS

volunteer_schedule = db.Table('volunteer_schedule',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('meetup_id', db.Integer, db.ForeignKey('events.meetup_id')),
    PrimaryKeyConstraint('meetup_id', 'user_id')
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(15))
    events = db.relationship('Event', secondary=volunteer_schedule,
                             backref=db.backref('events'))


    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0} {1}>'.format(self.first_name, self.last_name)

    def get_event(self, meetup_id):
        result = [event for event in self.events if event.meetup_id == meetup_id]
        result = result[0] if result else None
        return result

    def add_event(self, meetup_id):
        event = Event.query.get(meetup_id)
        if event:
            self.events.append(event)
            db.session.commit()

    def remove_event(self, meetup_id):
        event = Event.query.get(meetup_id)
        if event:
            self.events.remove(event)
            db.session.commit()

    def get_token(self, expiration=1800):
        s = Serializer(app.secret_key)
        return s.dumps(self.id).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.secret_key)
        try:
            id = s.loads(token)
        except:
            return None
        if id:
            return User.query.get(id)
        return None

class Event(db.Model):
    __tablename__ = 'events'
    # id = db.Column(db.Integer, primary_key=True)
    meetup_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120))
    event_url = db.Column(db.String(80))
    start_time = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    attendee_count = db.Column(db.Integer)

    def __init__(self, meetup_id, name, event_url, start_time, duration, attendee_count):
        self.meetup_id = meetup_id
        self.name = name
        self.event_url = event_url
        self.start_time = start_time
        self.duration = duration
        self.attendee_count = attendee_count

    def __repr__(self):
        return '<Event {0} {1}>'.format(self.meetup_id, self.name)

    @property
    def total_volunteers(self):
        return self.attendee_count / 10

    @property
    def num_volunteers(self):
        sql = "SELECT * FROM volunteer_schedule WHERE meetup_id = {0}".format(self.meetup_id)
        return len(db.session.query(volunteer_schedule).from_statement(text(sql)).all())

    def need_more_volunteers(self):
        return not self.num_volunteers == self.total_volunteers

    @property
    def num_volunteers_needed(self):
        return self.total_volunteers - self.num_volunteers

class RegistrationEmail(object):
    def __init__(self, recipient, recipient_email, event, venue_name, address):
        self.recipient = recipient
        self.recipient_email = recipient_email
        self.event = event
        self.venue_name = venue_name
        self.address = address
        self.url_escaped_address = urllib.quote_plus(self.address)
        self.html_text = self.build_html_text()

    def build_html_text(self):
        base_text = 'Greetings {0}, <br><br>You\'re confirmed to volunteer for the following event:</b><br><p>' \
                         '<b>Event:</b> <a href="{1}">{2}</a><br><b>Date: </b>{3}<br><b>Location: ' \
                         '</b>{4}, {5}<br><br>'.format(self.recipient, self.event.event_url, self.event.name,
                                                get_human_readable_date(self.event.start_time), self.venue_name, self.address)
        location_text = '<a href="https://www.google.com/maps/place/{0}">' \
                        '<img src="https://maps.googleapis.com/maps/api/staticmap?center={1}&zoom=14&size=300x300&markers=size:large|color:0xF9043C|label:P|{2}" /></a>'\
                        .format(self.url_escaped_address, self.url_escaped_address, self.url_escaped_address)

        closing_text = '<br><br>Please arrive at least fifteen minutes in advance. Any questions email or ' \
                            '<a href="http://twitter.com/home/?status=@PyLadiesChicago+help+re:{0}">Tweet us.</a> ' \
                            'We look forward to seeing you at the event.<br><br>Thanks for all you do! ' \
                            '<br><br>Catherine, Celeen, Lorena, & Safia <br><br><br>' \
                            '<img src="http://i.imgur.com/TddsutV.png" style="max-height:100px;" />'.format(self.event.name)
        html_text = base_text + location_text + closing_text
        return html_text

    def send(self):
        send_email(subject="You're confirmed to Volunteer for {0}".format(self.event.name),
                   sender=ADMINS[0],
                   recipients=[self.recipient_email],
                   text_body='Thank you {0} for registering to volunteer for {1}'.format(self.recipient, self.event.name),
                   html_body=self.html_text)

class DeregistrationEmail(object):
    def __init__(self, recipient_email, event):
        self.recipient_email = recipient_email
        self.event = event

    def send(self):
        send_email(subject= "You've unregistered to Volunteer for {0}".format(self.event.name),
                   sender= ADMINS[0],
                   recipients= [self.recipient_email],
                   text_body= "You've successfully unregistered to Volunteer for {0}".format(self.event.name),
                   html_body= "You've successfully unregistered to volunteer for <a href='{0}'>{1}</a>."
                              "<br>Hope to see you at another event soon!<br><br>Catherine, Celeen, Lorena, & Safia<br><br><br>" \
                              "<img src='http://i.imgur.com/TddsutV.png' style='max-height:100px;' />".format(self.event.event_url, self.event.name))

