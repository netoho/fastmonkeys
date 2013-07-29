from flask.ext.wtf import (Form, TextField, TextAreaField, PasswordField, SubmitField, Required, ValidationError,
                           BooleanField, HiddenField, RecaptchaField)

__author__ = 'netoho'


class PostForm(Form):
    title = TextField("Title", validators=[Required()])
    body = TextAreaField("Content", validators=[Required()])
    tags = HiddenField()
