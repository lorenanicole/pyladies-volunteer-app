from datetime import datetime
from app import app, db
from app.forms import ContactForm, ResetPasswordForm, ForgotPasswordForm, RegisterForm
from app.models import User, Event, RegistrationEmail, DeregistrationEmail
from flask import request, session, redirect, url_for, \
     render_template, flash, get_flashed_messages, jsonify
from app.emails import send_email, send_password_recovery_email
from helpers import get_meetup_events, get_meetup_address, get_user
from flask_negotiate import produces
from sqlalchemy.sql import text

@app.route('/')
@app.route('/index')
def index():
    events = Event.query.filter(Event.start_time >= int(datetime.utcnow().strftime("%s"))).all()
    if events:
        events = sorted(events, key=lambda e: e.start_time) # Sort events based on start time

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
            flash(["Umm ... Houston we have a problem.",'No user with that email exists. Please sign up.'])
            return redirect(url_for("signup"))


        if not user.password == request.form['password']:
            flash(["Umm ... Houston we have a problem.",'Incorrect password. Please try again.'])
            return render_template("login.html")

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
    form = RegisterForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(['A user with that email already exists. Please try again.'])
            return render_template("signup.html", form=form)

        if not user and form.validate_on_submit():
            user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully signed up!')
            return redirect(url_for('index'))

    return render_template("signup.html", form=form)

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
    event = Event.query.get(meetup_id)

    if volunteer_event:
        user.remove_event(meetup_id)
        deregistration_email = DeregistrationEmail(recipient_email=user.email, event=volunteer_event)
        deregistration_email.send()
        return jsonify({'volunteering': 'no',
                        'volunteers_needed': event.num_volunteers_needed,
                        'event_full': not event.need_more_volunteers()})

    if event.need_more_volunteers():
        user.add_event(meetup_id)
        address, name = get_meetup_address(meetup_id)
        confirmation_email = RegistrationEmail(recipient=user.first_name, recipient_email=user.email,
                                               event=user.get_event(meetup_id), venue_name=name, address=address)
        confirmation_email.send()
        return jsonify({'volunteering': 'yes',
                        'event_full': not event.need_more_volunteers(),
                        'volunteers_needed': event.num_volunteers_needed})
    else:
        return jsonify({'volunteering': 'no',
                'event_full': not event.need_more_volunteers(),
                'volunteers_needed': event.num_volunteers_needed})

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_recovery_email(user)
            flash(message="A password recovery email has been sent to the email listed on the user.")
            return redirect(url_for('index'))
        else:
            flash(message="There is no record of a user with that email.")
            return redirect(url_for('index'))

    return render_template('trigger_reset.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def validate_reset_password(token):
    form = ResetPasswordForm()
    user = User.verify_token(token)

    if request.method == "GET":
        if user:
            return render_template("reset.html", form=form, token=token)
        else:
            flash("Reset password failed. Please try again.")
            return redirect(url_for('index'))

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Success! You have changed your password oh wise PyLady!")
        return redirect(url_for('index'))

    flash("Reset password failed. Please try again.")
    return redirect(url_for('index'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        send_email(subject= form.subject.data,
                   sender= form.email.data,
                   recipients= app.config['ADMINS'],
                   text_body= "Request Type: {0} {1} From: {2}".format(form.type.data, form.message.data, form.email.data),
                   html_body= "<h3>Request Type: {0} </h3>".format(form.type.data) +
                              "<br><h3>From: {0}</h3><p>{1}</p>".format(form.email.data, form.message.data.strip()))
        flash('Your request form has been successfully sent. Thank you!')
        return redirect(url_for('index'))

    return render_template('contact.html', form=form)

