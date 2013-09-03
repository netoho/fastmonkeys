from app import login_manager
from app import (app, db)
from app.posts.models import Post
from app.tags.models import Tag
from app.posts.forms import PostForm
from flask.ext.login import login_required
from flask import (Blueprint, session, redirect, url_for,
                   render_template, flash, request)
import re

import math

__author__ = 'netoho'
mod = Blueprint('posts', __name__, url_prefix='/posts')

NUM_PAGES = 5

@mod.route('/', methods=['GET'])
@mod.route('/page/<int:page>')
def list_posts(page=1):
    posts = Post.query.order_by('pub_date asc').paginate(page, NUM_PAGES, False).items
    if 'number_of_posts' not in session:
        session['number_of_posts'] = len(Post.query.all())
    num_pages = int(math.ceil(float(session['number_of_posts']) / NUM_PAGES))
    return render_template('posts/posts.html', posts=posts, num_pages=num_pages, page=page)


@mod.route('/<int:id>')
def show_post(id):
    post = Post.query.get(id)
    if post == None:
        flash("Post not found")
        return redirect(url_for('posts.list_posts'))
    else:
        return render_template('posts/show.html', post=post)


@mod.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        tags_names = form.tags.data
        tags = []
        if ',' in tags_names:
            tags_names = tags_names.split(',')
        elif tags_names == '':
            tags_names = []
        else:
            tags_names = [tags_names]
        if len(tags_names) == 1:
            if Tag.query.filter_by(name=tags_names[0]).first():
                tags.append(Tag.query.filter_by(name=tags_names[0]).first())
            else:
                new_tag = Tag(tags_names[0])
                tags.append(new_tag)
                db.session.add(new_tag)
                db.session.commit()
        else:
            for tag_name in tags_names:
                if Tag.query.filter_by(name=tag_name).first():
                    tags.append(Tag.query.filter_by(name=tag_name).first())
                else:
                    new_tag = Tag(tag_name)
                    tags.append(new_tag)
                    db.session.add(new_tag)
                    db.session.commit()
        post = Post(title=form.title.data, body=form.body.data, tags=tags)
        db.session.add(post)
        db.session.commit()
        session['number_of_posts'] = len(Post.query.all())
        flash("Post created successfully")
        return redirect(url_for('posts.list_posts'))
    else:
        return render_template('posts/form.html', form=form, url=url_for('posts.new_post'))


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        tags_names = form.tags.data
        tags = []
        if ',' in tags_names:
            tags_names = tags_names.split(',')
        elif tags_names == '':
            tags_names = []
        else:
            tags_names = [tags_names]
        # if len(tags_names) == 1:
        #     if Tag.query.filter_by(name=tags_names[0]).first():
        #         tags.append(Tag.query.filter_by(name=tags_names[0]).first())
        #     else:
        #         new_tag = Tag(tags_names[0])
        #         tags.append(new_tag)
        #         db.session.add(new_tag)
        #         db.session.commit()
        # else:
        for tag_name in tags_names:
            if Tag.query.filter_by(name=tag_name).first():
                tags.append(Tag.query.filter_by(name=tag_name).first())
            else:
                new_tag = Tag(tag_name)
                tags.append(new_tag)
                db.session.add(new_tag)
                db.session.commit()
        post.title = form.title.data
        post.body = form.body.data
        post.tags = tags
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully")
        return redirect(url_for('posts.list_posts'))
    else:
        return render_template('posts/form.html', form=form, url=url_for('posts.edit_post', id=post.id),
                               post_id=post.id)


@mod.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('posts.list_posts'))


@mod.route('/search/')
@mod.route('/search/<int:page>')
def search_post(page=1):
    text = request.values.get('q')
    query = ""
    for word in filter(lambda t: t!="", text.split(" ")):
        query+=word+" & "
    q = " SELECT * FROM post WHERE to_tsvector('english', body || title ) @@ to_tsquery('english', '%s')" % query[0:-3]
    posts = Post.query.from_statement(q).all()
    for post in posts:
        text_lower = [w.lower() for w in text.split(" ")]
        body_span = ["<span style='background-color: yellow'>"+word+"</span>" if word.lower() in text_lower else word for word in re.findall(r"[\w']+", post.body)]
        post.body = " ".join(body_span)
        title_span = ["<span style='background-color: yellow'>"+word+"</span>" if word.lower() in text_lower else word for word in re.findall(r"[\w']+", post.title)]
        post.title = " ".join(title_span)
    num_pages = int(math.ceil(float(len(posts)) / NUM_PAGES))
    flash('Results for %s' % text)
    return render_template('posts/search.html', posts=posts[(page-1)*NUM_PAGES:(page*NUM_PAGES)], num_pages=num_pages, page=page, text=text)