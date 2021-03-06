from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Length, EqualTo, Email, email_validator

class RegisterForm(FlaskForm):
    name = StringField(
        'Username',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )


class LoginForm(FlaskForm):
    name = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

class UpdateAccountForm(FlaskForm):
    name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])