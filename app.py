from flask import Flask, request, jsonify, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUser

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedback'
app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///feedback.db'}

app.debug = True
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPTS_REDIRECTS'] = False

connect_db(app)
app.app_context().push()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register')
def register():
    form = RegisterUser()
    # return 'fart'
    return render_template('register.html', form=form)