"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route('/users')
def user_list():
    """Show a list of all users."""

    users = User.query.all()

    return render_template('user_list.html',
                            users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """ Registration form """

    return render_template('register_form.html')

@app.route('/register', methods=["POST"])
def register_process():
    """ Process registration """

    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    user = User(email=email,
                password=password,
                age=age,
                zipcode=zipcode)

    db.session.add(user)
    db.session.commit()

    flash('Yay! Successfully added!')

    return redirect('/')

@app.route('/login')
def login():
    """Renders log in page"""

    return render_template('login.html')

@app.route('/logged-in')
def check_logged_in():
    """Check if use is in database and login if is"""

    email = request.args.get("email")
    password = request.args.get("password")

    user_object = User.query.filter_by(email=email).first()

    if user_object:
        if user_object.password == password:
            session["login"] = True
            flash(f"Hey, welcome back {user_object.email} of zipcode {user_object.zipcode}")
            return redirect("/")
        else:
            flash(f"""You're wrong. Are you even {user_object.email} of zipcode {user_object.zipcode}?
                      The password is actually {user_object.password}""")
            return redirect("/login")
    else:
        flash(f"""You're not real.""")
        return redirect("/login")

@app.route("/log-out")
def log_out():
    """Log user out"""
    session["login"] = False
    flash("Logged out")
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
