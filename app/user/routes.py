from flask import Blueprint, request, flash, redirect, render_template, url_for, jsonify
from app.user.forms import RegisterForm
from app.user.model import User
from flask_login import current_user
from app import mail, db
from flask_mail import Message
from flasgger import swag_from

user = Blueprint("user", __name__, template_folder="templates")


def notify_by_email(user):
    msg = Message(
        "Καλώς ήρθατε στην εφαρμογή Announcements!",
        recipients=[user.email],
    )
    msg.body = f"""Καλώς ήρθατε στην εφαρμογή Announcements
Γειά σου {user.name.givenName} {user.name.surName}
Η εγγραφή έγινε με την ιδιότητα {user.category.name}"""
    mail.send(msg)


@user.route("api/register", methods=["POST"])
@swag_from("swagger/register.yml")
def api_register():
    body = request.get_json()
    try:
        doc = User(**body).save()
        return jsonify(doc), 201
    except db.NotUniqueError:
        return jsonify(error="User or Email already exist"), 400
    except db.ValidationError as exc:
        return jsonify(error=exc.message), 400


@user.route("api")
@swag_from("swagger/get_users.yml")
def get_users():
    users = User.objects().exclude("id", "password")
    return jsonify(users), 200


@user.route("api/<username>")
@swag_from("swagger/get_user.yml")
def get_one_user(username):
    doc = User.objects(username=username).exclude("id", "password").first()
    if doc:
        return jsonify(doc), 200
    else:
        return jsonify(error="User not found"), 404


@user.route("api/<username>", methods=["PATCH"])
@swag_from("swagger/update_user.yml")
def update_user(username):
    body = request.get_json()
    doc = User.objects(username=username).first()
    if doc:
        try:
            updated_doc = {
                key: body[key]
                for key in ["category", "name", "email"]
                if key in body.keys()
            }
            doc.update(**updated_doc)
            return jsonify(doc), 200
        except db.NotUniqueError:
            return jsonify(error="Email already exists"), 400
        except db.ValidationError as exc:
            return jsonify(error=exc.message), 400
    else:
        return jsonify(error="User not found"), 404


@user.route("api/<username>", methods=["DELETE"])
@swag_from("swagger/delete_user.yml")
def delete_user(username: str):
    doc = User.objects(username=username).first()
    if doc:
        doc.delete()
        return jsonify(doc), 200
    else:
        return jsonify(error="User not found!"), 404


@user.route("/register", methods=["GET", "POST"])
def register_new_user():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            for field, value in form.data.items():
                flash(f"{ field }: {value}", "info")
            newuser = User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                category={"name": form.category.data},
                name={"surName": form.surname.data, "givenName": form.givenname.data},
            ).save()
            # try:
            #     notify_by_email(newuser)
            # except Exception as exc:
            #     flash(f"Πρόβλημα αποστολής email στο {newuser.email}")
            # return redirect("/index")
        else:
            for field, error in form.errors.items():
                flash(f"Λάθος στο {field}: {error[0]}", "error")
    return render_template("register.html", title="Register", form=form)


@user.route("/profile")
def user_profile():
    return render_template("profile.html", title="User Profile")
