from __future__ import print_function
from flask import Blueprint, render_template, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
import os

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'posts2.db')
# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String)
    image = db.Column(db.String)
    text = db.Column(db.String)
    username = db.Column(db.String)#, nullable=False)
    verified = db.Column(db.Boolean)
    avatar = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #C reate a function to return a string when we add something
    def __repr__(self):
        return '<displayName %r>' % self.id 

@app.route('/<displayName>/<text>')
def index(displayName, text):
    posts = Posts(displayName=displayName, text=text)
    db.session.add(posts)
    db.session.commit()
    return '<h1>IT WORKS!</h1>'

@app.route("/home")
def my_index():
    #tweet = generator()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)