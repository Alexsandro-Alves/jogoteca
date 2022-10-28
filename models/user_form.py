from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class UserForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    password = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')