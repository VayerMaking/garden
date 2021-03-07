from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
import os
from datetime import datetime
#import hashlib


app = Flask(__name__)
#app.config['SECRET_KEY'] = config.secret_key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(150))

    #def verify(self, thing_to_verify):
    #    return self.thing_to_verify == hash_password(thing_to_verify)

#def hash(thing_to_hash):
#    return hashlib.sha256(thing_to_hash.encode('utf-8')).hexdigest()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/paypal', methods=['GET'])
def paypal():
    return render_template('paypal.html')

@app.route('/preorder', methods=['GET', 'POST'])
def preorder():
    if request.method == "POST":
        data = request.form
        print(data['name'], data['email'], data['address'])
        user = User(name=data['name'], email=data['email'], address=data['address'])
        db.session.add(user)
        db.session.commit()

        return render_template('succesfull_preorder.html', name=user.name)
    elif request.method == "GET":

        return render_template("preorder.html")
    #return render_template('preorder.html')
db.create_all()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True)
	#app.run(debug=True)
