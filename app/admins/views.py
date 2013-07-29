from app import login_manager
from app.admins.models import Admin
from app import (app, db)
from flask.ext.login import login_required
from flask import (Blueprint, session, redirect, url_for,
                   render_template, flash)


__author__ = 'netoho'
mod = Blueprint('admins', __name__, url_prefix='/admins')


@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))
