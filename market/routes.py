from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User, Visit, Answer
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/visits')
def visits_page():
    posts = Visit.query.all()
    return render_template('visits.html', items=posts)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        check_user = User.query.filter_by(username=login_form.username.data).first()
        if check_user and check_user.check_password_correction(
                attempted_password=login_form.password.data
        ):
            login_user(check_user)
            flash(f'Great, everything is ok! You are login as: {check_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Please provide correct data.', category='danger')

    return render_template('login.html', form=login_form)


@app.route('/posts')
def posts_page():
    posts = Item.query.all()
    answers = Answer.query.all()
    return render_template('posts.html', items=posts, answers=answers)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        create_user = User(username=register_form.username.data,
                              email_address=register_form.email_address.data,
                              password=register_form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        return redirect(url_for('posts_page'))
    # if no error during register new account
    if register_form.errors != {}:
        # if error during register new account
        for _ in register_form.errors.values():
            flash(f'Error, : {_}', category='danger')
    return render_template('register.html', form=register_form)
