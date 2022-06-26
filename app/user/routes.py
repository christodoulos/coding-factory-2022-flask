from flask import Blueprint, request, flash, redirect, render_template, url_for
from app.user.forms import RegisterForm
from app.user.model import User
from flask_login import current_user

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/register", methods=["GET", "POST"])
def register_new_user():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            for field, value in form.data.items():
                flash(f"{ field }: {value}", "info")
            User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                category={"name": form.category.data},
                name={"surName": form.surname.data, "givenName": form.givenname.data},
            ).save()
            return redirect("/index")
        else:
            for field, error in form.errors.items():
                flash(f"Error in {field}: {error[0]}", "error")
    return render_template("register.html", title="Register", form=form)


@user.route("/profile")
def user_profile():
    return render_template("profile.html", title="User Profile")
