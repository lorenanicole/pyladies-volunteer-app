import uuid
from flask.ext.wtf import Form
from wtforms import SelectField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


def _generate_csrf_token():
    return str(uuid.uuid4())

class RegisterForm(Form):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Send")

class ContactForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    type = SelectField(u'Request Type', choices=[('Sponsor', 'Sponsor PyLadies'), ('Host', 'Host an Event'), ('Talk', 'Give a Talk'),
                                               ('Workshop', 'Lead a Workshop'), ('Media', 'Media Inquiries'), ('Other', 'Other')])
    submit = SubmitField("Send")

class ResetPasswordForm(Form):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Send")

class ForgotPasswordForm(Form):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Send")