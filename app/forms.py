from wtforms import SelectField, Form, TextAreaField, SubmitField, StringField


class ContactForm(Form):
  name = StringField("Name")
  email = StringField("Email")
  subject = StringField("Subject")
  message = TextAreaField("Message")
  type = SelectField(u'Request Type', choices=[('sponsor', 'Sponsor PyLadies'), ('host', 'Host an Event'), ('talk', 'Give a Talk'),
                                               ('workshop', 'Lead a Workshop'), ('media', 'Media Inquiries'), ('other', 'Other')])
  submit = SubmitField("Send")