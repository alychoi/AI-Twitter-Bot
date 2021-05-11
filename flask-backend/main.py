from __future__ import print_function
from flask import Blueprint, render_template, Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_session import Session
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
import os
import logging

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask("__name__")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'posts2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)
ma = Marshmallow(app)

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
    def __init__(self, id, displayName, image, text, username, verified, avatar):
        self.id = id
        self.displayName = displayName
        self.image = image
        self.text = text
        self.username = username
        self.verified = verified
        self.avatar = avatar

@app.route('/<displayName>/<text>')
def index(displayName, text):
    posts = Posts(displayName=displayName, text=text)
    db.session.add(posts)
    db.session.commit()
    return '<h1>IT WORKS!</h1>'

class PostsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'displayName', 'image', 'text', 'username', 'verified', 'avatar', 'date_created')

post_schema = PostsSchema()
posts_schema = PostsSchema(many=True)

@app.route("/api", methods = ['GET', 'POST'])
def api():
    #tweet = generator()
    if request.method == 'POST':
        id = Posts.query.order_by('id').all()[-1].id + 1
        displayName = request.json['displayName'] 
        image = request.json['image'] 
        text = request.json['text'] 
        username = request.json['username'] 
        verified = request.json['verified']
        avatar = request.json['avatar']
        #date_created = request.json['date_created']
        new_posts = Posts(id, displayName, image, text, username, verified, avatar)
        db.session.add(new_posts)
        db.session.commit()
        print(new_posts)
        return post_schema.jsonify(new_posts)
    elif request.method == 'GET':
        all_posts = Posts.query.all()
        result = posts_schema.dump(all_posts)
        print(result)
        return jsonify(result)
    else:
        return render_template('index.html')

@app.route("/home")
def my_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)