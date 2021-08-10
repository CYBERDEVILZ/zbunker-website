from zbunker import app, db
from flask import render_template, redirect, flash, url_for, request
from zbunker.forms import LoginForm, RegistrationForm
from zbunker.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def landing():
    return render_template("landing.html", title="Landing")


@app.route("/home")
def home():
    videos = [1, 2, 3, 4, 5, 6, 7]
    return render_template("home.html", videos=videos)


@app.route("/prime", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("prime.html", title="Prime", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remMe.data)
            nextPage = request.args.get("next")
            return redirect(nextPage) if nextPage else redirect(url_for("home"))

        else:
            flash(
                "Login Unsuccessful. Please check email and password", category="danger"
            )

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/pt")
def pt():
    form = RegistrationForm()
    return render_template("pt.html", form=form)


@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@app.route("/basic")
def basic():
    title = "Basic"
    return render_template("basic.html", title=title)


@app.route("/learn/ethical-hacking")
def eth():
    title = "Ethical Hacking"
    return render_template("eth.html", title=title)


@app.route("/learn/python-programming")
def pythonprogramming():
    title = "Python Programming"
    return render_template("python.html", title=title)