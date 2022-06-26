from flask import redirect, render_template, flash, request
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
    if request.method == "POST":
        if form.validate_on_submit():
            flash(f"Login requested for user {form.username.data}", "info")
            flash(f"remember_me={form.remember_me.data}", "info")
            return redirect("/index")
        else:
            for field, error in form.errors.items():
                flash(f"Error in {field}: {error[0]}", "error")
    return render_template("login.html", title="Sign In", form=form)
