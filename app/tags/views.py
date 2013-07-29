from app import login_manager
from app import (app, db)
from app.tags.models import Tag
from app.posts.models import Post
from app.tags.forms import TagForm
from flask.ext.login import login_required
from flask import (Blueprint, session, redirect, url_for,
                   render_template, flash, jsonify, request)


__author__ = 'netoho'

mod = Blueprint('tags', __name__, url_prefix='/tags')


@mod.route('/new', methods=['GET', 'POST'])
@login_required
def new_tag():
    form = TagForm()
    return render_template('tags/form.html', form=form)


@mod.route('/', methods=['GET', 'POST'])
def tags():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(form.name.data)
        db.session.add(tag)
        db.session.commit()
    tags = Tag.query.all()
    return render_template('tags/tags.html', tags=tags, form=form)


@mod.route('/<int:id>')
def show_tag(id):
    tag = Tag.query.get(id)
    posts = tag.posts.all()
    return render_template('tags/show.html', tag=tag, posts=posts)

@mod.route('/delete/<int:id>')
@login_required
def delete_tag(id):
    tag = Tag.query.get(id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags.tags'))


@mod.route('/json/<int:id>')
@mod.route('/json/')
def json_tags(id=0):
    tags = Tag.query.all()
    a_tags = []
    if id != 0:
        a_tags = Post.query.get(id).tags
    di = dict(((lambda t: t.id)(t), t.name) for t in tags)
    avt = map(lambda t: t.name, tags)
    ast = map(lambda t: t.name, a_tags)
    return jsonify(availableTags=avt, assignedTags=ast)