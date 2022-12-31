from flask import Flask, request, jsonify, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUser
from sqlalchemy.exc import IntegrityError




app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedback'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_feedback.db'}

app.debug = False
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPTS_REDIRECTS'] = False

connect_db(app)
app.app_context().push()

@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User(
            username=username,
            password=password,
            email=email,
            first_name= first_name,
            last_name = last_name
        )
        
        db.session.add(new_user)
            
        try:
            db.session.commit()
            
        except IntegrityError:
            form.user.errors.append('Username already exists. Please choose another')
            return render_template('register.html')
        flash('SUCCESS! USER CREATED')
        return redirect('/')
    return render_template('register.html', form=form)

