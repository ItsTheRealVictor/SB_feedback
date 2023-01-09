from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from datetime import datetime



app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedback'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_feedback.db'}

# use this DB when developing from work computer
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'


app.debug = False
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPTS_REDIRECTS'] = False

connect_db(app)
app.app_context().push()

@app.route('/')
def home():
    all_feedback = Feedback.query.all()
    return render_template('home.html', all_feedback=all_feedback)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        register_new_user = User.register_user(username, password, email, first_name, last_name)
        
        db.session.add(register_new_user)
            
        try:
            db.session.commit()
            
        except IntegrityError:
            form.user.errors.append('Username already exists. Please choose another')
            return render_template('register.html')
        flash('SUCCESS! USER CREATED')
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate_user(username, password)
        if user:
            flash(f'Welcome back {user.first_name}')
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye')
    return redirect('/')

@app.route('/secret')
def secret():
    if 'username' not in session:
        flash('You need to be logged in to see this')
        return redirect('/')
    else:
        return render_template('secret.html')

@app.route('/users/<username>', methods=['GET', 'POST'])
def show_user_info(username):
    user = User.query.get_or_404(username)
    if 'username' not in session:
        flash('You need to be logged in to see this')
        return redirect('/')
    else:
        return render_template('user_info.html', user=user)
    
@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    form = FeedbackForm()
    user = User.query.get_or_404(username)
     
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        new_feedback = Feedback(title=title, content=content, username=session['username'])
        # breakpoint()
        db.session.add(new_feedback)
        db.session.commit()
        flash('FEEDBACK CREATED')
        return redirect(f'/users/{user.username}')
        
        
    
    return render_template('add_feedback.html', form=form, user=user)

@app.route('/users/<username>/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(username, feedback_id):
    username = User.query.get_or_404(username)
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('FEEDBACK DELETED')
        return redirect(f'/users/{username.username}')
    
    
    return render_template('delete_feedback.html', username=username, feedback=feedback)

@app.route('/users/<username>/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(username, feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)