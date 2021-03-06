from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime


app = Flask(__name__)
#app.config['SECRET_KEY'] = config.secret_key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
	#app.run(debug=True)
