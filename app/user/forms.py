from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField("Όνομα χρήστη", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    category = StringField("Κατηγορία προσωπικού", validators=[DataRequired()])
    givenname = StringField("Όνομα", validators=[DataRequired()])
    surname = StringField("Επώνυμο", validators=[DataRequired()])
    password = PasswordField(
        "Κωδικός",
        validators=[
            DataRequired(),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Επανάληψη κωδικού")
    submit = SubmitField("Εγγραφή")
