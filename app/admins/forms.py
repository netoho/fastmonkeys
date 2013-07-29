from flask.ext.wtf import (Form, TextField, TextAreaField, PasswordField, SubmitField, Required, ValidationError,
                           BooleanField, HiddenField, RecaptchaField)

__author__ = 'netoho'


class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)