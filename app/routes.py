from flask import redirect, render_template, flash, url_for
from app import announcements_app
from app.forms import LoginForm
from app.user.model import User
from flask_login import current_user, login_user, logout_user


@announcements_app.route("/")
@announcements_app.route("/index")
def index():
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
    return render_template("index.html", title="Home", announcements=announcements)


@announcements_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash(f"Λάθος όνομα χρήστη ή κωδικός", "error")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash(
            f"Συνδεδεμένος χρήστης: {user.name.givenName} {user.name.surName}", "info"
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@announcements_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
