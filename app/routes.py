from flask import redirect, render_template, flash, request
from app import announcements_app
from app.forms import LoginForm, RegisterForm
from app.models import User


@announcements_app.route("/")
@announcements_app.route("/index")
def index():
    user = {"username": "christodoulos"}
    announcements = [
        {
            "department": "Γραμματεία Σχολής Πολιτικών Μηχανικών",
            "subject": "Έναρξη εγγραφών στο εξάμηνο",
        },
        {
            "department": "Διεύθυνση Οικονομικών Υπηρεσιών",
            "subject": "Προκυρήξεις Διαγωνισμών",
        },
    ]
    return render_template(
        "index.html", title="Home", user=user, announcements=announcements
    )


@announcements_app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}")
        flash(f"remember_me={form.remember_me.data}")
        return redirect("/index")
    return render_template("login.html", title="Sign In", form=form)


@announcements_app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash(f"Form data: {form.data}")
            User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                category={"name": form.category.data},
                name={"surName": form.surname.data, "givenName": form.givenname.data},
            ).save()
            return redirect("/index")
        else:
            flash(f"Form data invalid: {form.errors}")
    return render_template("register.html", title="Register", form=form)
