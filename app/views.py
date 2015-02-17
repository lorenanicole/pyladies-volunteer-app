import random
from sqlite3 import IntegrityError
from datetime import datetime
from app import app, db
from app.forms import ContactForm
from app.models import User, Event, volunteer_schedule, RegistrationEmail, DeregistrationEmail
from flask import request, session, redirect, url_for, abort, \
     render_template, flash, get_flashed_messages, jsonify
from app.emails import send_email
from app.settings import ADMINS
from helpers import get_meetup_events, get_meetup_address, get_human_readable_date, get_user
from flask_negotiate import consumes, produces


@app.route('/')
@app.route('/index')
def index():
    events = db.session.query(Event).filter(Event.start_time >= int(datetime.utcnow().strftime("%s"))).all()
    if events:
        events = sorted(events,key=lambda e: e.start_time) # Sort events based on start time

    user = User.query.filter_by(email=session.get('email', None)).first()
    if user:
        volunteering = [event.meetup_id for event in user.events]
    else:
        volunteering = []

    return render_template("index.html", events=events, volunteering=volunteering)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()

        if not user:
            error = 'No user with that email exists. Please sign up.'
            return redirect(url_for("signup", error=error))


        if not user.password == request.form['password']:
            error = 'Incorrect password. Please try again.'
            return render_template("login.html", error=error)

        session['username'] = user.first_name
        session['user_id'] = user.id
        session['email'] = user.email

        return redirect(url_for('index'))

    return render_template("login.html")

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    error = request.args.get('error', None)
    if request.method == "POST":
        try:
            cursor = db.execute('INSERT INTO users(email, password, first_name, last_name) VALUES (?, ?, ?, ?)',
                            (request.form['email'], request.form['password'], request.form['first_name'], request.form['last_name']))
            db.commit()
            user = cursor.fetchall()
        except IntegrityError:
            error = 'A user with that email already exists. Please try again.'
            db.close()
            return render_template("signup.html", error=error)

        db.close()
        flash('You have successfully signed up!')
        messages = get_flashed_messages()
        return redirect(url_for('index'))

    return render_template("signup.html", error=error)

@app.route('/schedule', methods=['GET'])
def volunteer_schedule():
    if not 'user_id' in session:
        return redirect(url_for('index'))

    user = get_user(session['user_id'])
    events = user.events

    events = sorted(events,key=lambda e: e.start_time) # Sort events based on start time
    events = [event for event in events if event.start_time > int(datetime.utcnow().strftime("%s"))] # Don't show past events

    return render_template("schedule.html", events=events)

@app.route('/create_events', methods=['GET'])
def create_events():
    events = Event.query.all()

    if not events:
        event_ids = []
    else:
        event_ids = [event.id for event in events]

    new_events = get_meetup_events()

    for id, new_event in new_events.items():
        if id not in event_ids:
            event = Event(meetup_id=id, name=new_event['name'], event_url=new_event['event_url'],
                          start_time=new_event['start_time'], duration=new_event['duration'],
                          attendee_count=new_event['attendee_count'])
            db.session.add(event)
            db.session.commit()

    return redirect(url_for('index', events=new_events))

@produces('application/json')
@app.route('/<int:user_id>/rsvp_volunteer/<int:meetup_id>', methods=['POST'])
def rsvp_as_volunteer(user_id, meetup_id):
    user = get_user(user_id)
    volunteer_event = user.get_event(meetup_id)
    print volunteer_event

    if not volunteer_event:
        user.add_event(meetup_id)
        address, name = get_meetup_address(meetup_id)
        confirmation_email = RegistrationEmail(recipient=user.first_name, recipient_email=user.email,
                                               event=user.get_event(meetup_id), venue_name=name, address=address)
        confirmation_email.send()

        return jsonify({'volunteering': 1})

    user.remove_event(meetup_id)
    deregistration_email = DeregistrationEmail(recipient_email=user.email, event=volunteer_event)
    deregistration_email.send()

    return jsonify({'volunteering': 0})

@app.route('/test', methods=['POST','GET'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
      return 'Form posted.'

  return render_template('contact.html', form=form)

def test():
    new_user = User(first_name='another', last_name='test', email='test@me.com', password='123')
    db.session.add(new_user)
    db.session.commit()
    return "success"
    # return {'msg': send_email("test", ADMINS[0], ["lorena.n.mesa@gmail.com"], "this is a test", "<b>HTML</b> body")}

