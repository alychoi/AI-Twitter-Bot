from __future__ import print_function
from flask import Blueprint, render_template, Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_session import Session
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, desc
import os
import logging 
import random
import pickle

from keras.utils.np_utils import to_categorical
from keras import regularizers
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Dropout, Embedding, Flatten, Bidirectional, Input, LSTM
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.optimizers import Adam
from keras.metrics import categorical_accuracy, mean_squared_error, mean_absolute_error, logcosh
from keras.layers.normalization import BatchNormalization
from matplotlib import pyplot as plt
import numpy as np
import math
import random
import sys
import csv
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader
import sqlite3

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask("__name__")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
	os.path.join(basedir, 'posts2.db')
app.config['SQLALCHEMY_BINDS'] = {
	'quotes': 'sqlite:///' + os.path.join(basedir, 'quotes.db')}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

seq_length = 100
valid = """ ~#@!"$%&'()+,-./:?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"""
chars = sorted(list(set(valid)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_vocab = len(chars)

# define the LSTM model
filename = "weights-improvement-07-1.5498.hdf5"
model = load_model(filename)

def gen(raw_text):
	padding = max(0, seq_length-len(raw_text))
	input = ' '*padding + raw_text
	if len(raw_text)>seq_length:
		input = input[len(input)-seq_length:]
	pattern = [char_to_int[char] for char in input]
	for i in range(280-len(raw_text)):
		x = np.reshape(pattern, (1, len(pattern), 1))
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)
		index = np.argmax(prediction)
		result = int_to_char[index]
		raw_text += result
		seq_in = [int_to_char[value] for value in pattern]
		pattern.append(index)
		pattern = pattern[1:]
	print("raw_text: " + raw_text)
	if raw_text.count('https://t.co/qDlFBGMeag')>1:
		raw_text = raw_text[:raw_text.find('https://t.co/qDlFBGMeag')+len('https://t.co/qDlFBGMeag')]
	if len(raw_text)>280:
		raw_text=raw_text[:280]
	print("final_raw_text: " + raw_text)
	return raw_text

# Create db model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	displayName = db.Column(db.String)
	image = db.Column(db.String)
	text = db.Column(db.String)
	username = db.Column(db.String)#, nullable=False)
	verified = db.Column(db.Boolean)
	avatar = db.Column(db.String)
	#comments = db.Column(db.PickleType)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __init__(self, id, displayName, image, text, username, verified, avatar):
		self.id = id
		self.displayName = displayName
		self.image = image
		self.text = text
		self.username = username
		self.verified = verified
		self.avatar = avatar
		#self.comments = comments

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
		#print(request.get_json())
		image = request.json['image'] 
		text = request.json['text'] 
		username = request.json['username'] 
		verified = request.json['verified']
		avatar = request.json['avatar']
		new_posts = Posts(id, displayName, image, text, username, verified, avatar)
		db.session.add(new_posts)
		db.session.commit()
		return post_schema.jsonify(new_posts)
	if request.method == 'GET':
		all_posts = Posts.query.order_by(desc(Posts.id))
		result = posts_schema.dump(all_posts)
		print()
		return jsonify(result)

class Quotes(db.Model):
	__bind_key__ = 'quotes'
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String)
	text = db.Column(db.String)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __init__(self, id, category, text):
		self.id = id
		self.category = category
		self.text = text

class QuotesSchema(ma.Schema):
	class Meta:
		fields = ('id', 'category', 'text')

quote_schema = QuotesSchema()
quotes_schema = QuotesSchema(many=True)

@app.route("/api-quotes", methods = ['GET', 'POST'])
def apiquotes():
	#tweet = generator()
	#curr = gen("There once was a ")
	items = ['Good days will come.', 'Keep calm and carry on!',
	'Treat others the way you want to be treated', 'Life is meaningless without happiness',
	'They may have talent, but you have determination']
	if request.method == 'POST':
		curr = gen("There once was a ")
		id = Quotes.query.order_by('id').all()[-1].id + 1
		category = 'quotes' 
		text = curr
		print("THIS IS THE TEXT!!!!! ->>>>" + text)
		#text = items[random.randrange(len(items))]
		new_quotes = Quotes(id, category, text)
		db.session.add(new_quotes)
		db.session.commit()
		return quote_schema.jsonify(new_quotes)
	if request.method == 'GET':
		samp = gen("There once was a ")
		print("THIS IS THE TEXT!!!!! ->>>>" + samp)
		all_quotes = Quotes.query.order_by(desc(Quotes.id))
		result = quotes_schema.dump(all_quotes)
		return jsonify(result)

@app.route("/home", methods = ['GET'])
def my_index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
