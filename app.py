import datetime
import os

from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy.exc import IntegrityError
from forms import SignupForm

from models import Signups
from database import db_session, init_db

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', "secret")


@app.route("/", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        signup = Signups(name=form.name.data,
                         email=form.email.data,
                         date_signed_up=datetime.datetime.now())
        db_session.add(signup)
        try:
            db_session.commit()
        except IntegrityError:
            return "User Already Exists"
        return redirect(url_for('success', _external=True))
    return render_template('signup.html', form=form)


@app.route("/success")
def success():
    if request.method == "GET":
        signups = Signups.query.order_by('id').all()
        response = []
        for signup in signups:
            signup = signup.__dict__
            del signup["_sa_instance_state"]
            response.append(signup)
        print(response)
        return render_template('success.html', signups=response)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5090)
