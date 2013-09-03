from flask.ext.wtf import (Form, TextAreaField, Required)

__author__ = 'netoho'


class MessageForm(Form):
    body = TextAreaField("Content", validators=[Required()])
