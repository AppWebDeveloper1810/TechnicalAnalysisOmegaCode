from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class SignUp(FlaskForm):
    name = StringField('Name', validators=[DataRequired("Data is required")])#
    email = StringField('Email', validators=[DataRequired("Data is required"), Email("You have not entered a valid email.")])#
    password = PasswordField('Password', validators=[DataRequired("Data is required")])#


class SignIn(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Data is required"), Email("You have not entered a valid email.")])#
    password = PasswordField('Password', validators=[DataRequired("Data is required")])#


class UpgradeForm(FlaskForm):
    plan = StringField(label="PLANS", validators=[DataRequired(message="Data is required")])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(label="Current Password", validators=[DataRequired(message="Password is empty")])
    new_password = PasswordField(label="New Password", validators=[DataRequired(message="Password is empty")])
