# imports
from functools import wraps
from flask import (flash, redirect, render_template,
    request, session, url_for, Blueprint)
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm, UpdateAccountForm
from project import db, bcrypt
from project.models import User, Follower
from project.users.utils import save_picture

# config
users_blueprint = Blueprint('users', __name__)

# helper functions

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return (redirect(url_for('users.login')))
    return wrap


# routes

@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('role', None)
    return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(user.password,
                request.form['password']):
                    session['logged_in'] = True
                    session['user_id'] = user.id
                    session['user_email'] = user.email
                    session['image_file'] = user.image_file
                    session['name'] = user.name
                    session['role'] = user.role
                    return redirect(url_for('tweets.tweet'))
            else:
                error = 'Invalid username or password.'
    return render_template('index.html', form=form, error=error)

@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if 'logged_in' in session:
        return redirect(url_for('tweets.tweet'))
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                bcrypt.generate_password_hash(form.password.data),
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'That username and/or email already exists.'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)

@users_blueprint.route('/users/')
@login_required
def all_users():
    users = db.session.query(User).all()
    return render_template('users.html', users=users)

@users_blueprint.route('/account/', methods=['GET', 'POST'])
@login_required
def accounts():
    error = None
    form = UpdateAccountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            userid = session['user_id']
            username = session['name']
            email = session['user_email']
            user = User.query.get(userid)
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            user.name = form.name.data
            user.email = form.email.data
            try:
                db.session.commit()
                session['name'] = user.name
                session['user_email']  = user.email
                username = session['name']
                email = session['user_email'] 
                image_file = url_for('static', filename='profile_pics/' + user.image_file)
                session['image_file'] = user.image_file
                flash('アカウントが更新されました')
                return render_template('account.html', form=form, username=username, 
                image_file=image_file, email=email )
            except IntegrityError:
                error = 'That username and/or email already exists.'
                image_file_from_session = session['image_file']
                image_file = url_for('static', filename='profile_pics/' + image_file_from_session)
                return render_template('account.html', form=form, error=error, username=username, 
                image_file=image_file, email=email )
    userid = session['user_id']
    username = session['name']
    email = session['user_email'] 
    user = User.query.get(userid)
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('account.html', form=form, username=username, image_file=image_file, email=email )