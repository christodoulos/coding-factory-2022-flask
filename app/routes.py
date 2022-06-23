from flask import redirect, render_template, flash
from app import announcements_app
from app.forms import LoginForm


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
