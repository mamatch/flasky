from flask import render_template, session, url_for, redirect
from . import main
from ..models import User
from .forms import NameForm
from .. import db
from datetime import datetime
from ..email import send_mail


@main.route("/", methods=["GET", "POST"])
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
        return redirect(url_for(".index"))
    return render_template(
        "index.html",
        current_time=datetime.utcnow(),
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )
