from flask import Flask, render_template, session, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime
import os
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SECRET_KEY"] = "djoumatchoua"  # Mandatory for wtf modules

# Configurations for the db engine
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["FLASKY_MAIL_SUBJECT_PREFIX"] = "[FLASKY]"
app.config["FLASKY_MAIL_SENDER"] = "Flasky Admin <dej@dej.com>"
app.config["FLASKY_ADMIN"] = os.environ.get("FLASKY_ADMIN")

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


@app.shell_context_processor  # Add context to the shell to not import always
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


# Mail functions


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


# ------------------- View functions --------------------


@app.errorhandler(404)
def page_not_found(e):  # Do not forget the error arg
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():  # Verify if the form has been submitted
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            if app.config["FLASKY_ADMIN"]:
                send_mail(app.config["FLASKY_ADMIN"], "New user", "new_user", user=user)
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        current_time=datetime.utcnow(),
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


@app.route("/user/<string:name>")
def get_user(name):
    return render_template("user.html", name=name)


# ---------------------------- Forms -----------------------------------


class NameForm(FlaskForm):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# ---------------------------- Models ----------------------------------


class Role(db.Model):
    __tablename__ = "roles"
    # SqlAlchemy always needs an id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship(
        "User", backref="role", lazy="dynamic"
    )  # To repr one-to-many

    def __repr__(self) -> str:
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # To repr the many-to-one relation
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username
