from flask.ext.wtf import (Form, TextField, TextAreaField, PasswordField, SubmitField, Required, ValidationError,
                           BooleanField, HiddenField, RecaptchaField)

__author__ = 'netoho'


class TagForm(Form):
    name = TextField("Name", validators=[Required()])