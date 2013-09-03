from app import login_manager
from app import (app, db)
from app.posts.models import Post
from app.messages.models import Message
from app.messages.forms import MessageForm
from flask.ext.login import login_required
from flask import (Blueprint, session, redirect, url_for,
                   render_template, flash, request)

import math

__author__ = 'netoho'
mod = Blueprint('messages', __name__, url_prefix='/messages')

NUM_PAGES = 5

@mod.route('/new', methods=['GET', 'POST'])
@login_required
def new_message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(body=form.body.data)
        db.session.add(message)
        db.session.commit()
        flash("Message created successfully")
        return redirect(url_for('posts.list_posts'))
    else:
        return render_template('posts/form.html', form=form, url=url_for('messages.new_message'))