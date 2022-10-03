from . import mail
from flask_mail import Message
from threading import Thread


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        app.config["FLASKY_MAIL_SUBJECT_PREFIX"] + subject,
        recipients=[to],
        sender=app.config["FLASKY_MAIL_SENDER"],
    )

    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr
