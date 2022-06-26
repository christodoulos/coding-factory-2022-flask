from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Όνομα χρήστη", validators=[DataRequired()])
    password = PasswordField("Κωδικός", validators=[DataRequired()])
    remember_me = BooleanField("Αποθήκευση στοιχείων")
    submit = SubmitField("Είσοδος")
