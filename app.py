from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
import os
from datetime import datetime
import hashlib


app = Flask(__name__)
#app.config['SECRET_KEY'] = config.secret_key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///todo.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(150))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    order_status = db.Column(db.String(100)) #order_status will possibly be edited manually through the db

    def verify(self, thing_to_verify):
        return self.thing_to_verify == hash_password(thing_to_verify)

def hash_password(thing_to_hash):
    return hashlib.sha256(thing_to_hash.encode('utf-8')).hexdigest()

def email_link(user_id):
    links = User.query.all()
    return links[user_id].email
    # when we get the email we should email a paypal link to it
    # verification of the payment probably will be done manually by a human

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = "Guest"
    return render_template('index.html', username=username)

@app.route('/paypal', methods=['GET'])
def paypal():
    return render_template('paypal.html')

@app.route('/products', methods=['GET'])
def products():
    return render_template('products.html')

@app.route('/preorder', methods=['GET', 'POST'])
def preorder():
    if request.method == "POST":
        data = request.form
        #print(data['name'], data['email'], data['address'])
        user = User.query.filter_by(username=session['username']).first()
        #user = User(name=data['name'], email=data['email'], address=data['address'])
        #should be an update not 2 separate instances of the class
        user.name = data['name']
        user.email = data['email']
        user.address = data['address']
        db.session.add(user)
        db.session.commit()

        return render_template('succesfull_preorder.html', name=user.name)
    elif request.method == "GET":

        return render_template("preorder.html")
    #return render_template('preorder.html')
@app.route('/email', methods=['GET'])
def email():
    return email_link(5)

@app.route('/status', methods=['GET'])
def status():
    user = User.query.filter_by(username=session['username']).first()
    print("order_status", user.order_status)
    return render_template('preorder_status.html', username=session['username'], order_status=user.order_status)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: throw a warning for usernames that are already used, bacause it would f*ck up preorder
    if request.method == "POST":
        data = request.form
        if not User.query.filter_by(username=data['username']).first():
            user = User(username=data['username'], password=hash_password(data['password']))
            db.session.add(user)
            db.session.commit()
        else:
            return "username not avaible"

        return render_template('login.html')
    elif request.method == "GET":

        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data['username'], password=hash_password(data['password'])).first()
        if not user:
            return render_template("login.html", message="invalid credentials")

        session['username'] = data['username']

        return redirect(('/'))

    elif request.method == "GET":
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

db.create_all()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)
