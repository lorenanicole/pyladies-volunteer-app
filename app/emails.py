from flask.ext.mail import Message
from app import mail, app


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_recovery_email(user):
    send_email(subject="Reset your Chicago PyLadies Volunteer Password",
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body="You have requested to reset your Chicago PyLadies Volunteer account password. "
                         "Please visit http://localhost:5000/reset_password/{0} to reset your password. "
                         "Thank you! - Chicago PyLadies".format(user.get_token()),
               html_body="<p>You have requested to reset your Chicago PyLadies Volunteer account password. "
                         "Please <a href='http://localhost:5000/reset_password/{0}'> click here </a> to reset your "
                         "password.<br><br>Catherine, Celeen, Lorena, & Safia</p><br><br><br>"
                         "<img src='http://i.imgur.com/TddsutV.png' style='max-height:100px;' />".format(user.get_token())
               )