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

from keras.utils.np_utils import to_categorical
from keras import regularizers
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout, Embedding, Flatten, Bidirectional, Input, LSTM
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.optimizers import Adam
from keras.metrics import categorical_accuracy, mean_squared_error, mean_absolute_error, logcosh
from keras.layers.normalization import BatchNormalization
from matplotlib import pyplot as plt
import numpy
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'posts2.db')
app.config['SQLALCHEMY_BINDS'] = {'quotes': 'sqlite:///' + os.path.join(basedir, 'quotes.db')}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    def __init__(self, id, displayName, image, text, username, verified, avatar):
        self.id = id
        self.displayName = displayName
        self.image = image
        self.text = text
        self.username = username
        self.verified = verified
        self.avatar = avatar

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
        print(request.get_json())
        image = request.json['image'] 
        text = request.json['text'] 
        username = request.json['username'] 
        verified = request.json['verified']
        avatar = request.json['avatar']
        new_posts = Posts(id, displayName, image, text, username, verified, avatar)
        db.session.add(new_posts)
        db.session.commit()
        print(db)
        return post_schema.jsonify(new_posts)
    if request.method == 'GET':
        all_posts = Posts.query.order_by(desc(Posts.id))
        result = posts_schema.dump(all_posts)
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
    items = ['Good days will come.', 'Keep calm and carry on!',
    'Treat others the way you want to be treated', 'Life is meaningless without happiness',
    'They may have talent, but you have determination']
    if request.method == 'POST':
        gen = generator()
        print("Post request to quotes")
        id = Quotes.query.order_by('id').all()[-1].id + 1
        category = 'quotes' 
        text = gen
        #text = items[random.randrange(len(items))]
        new_quotes = Quotes(id, category, text)
        print("Inserting to new_quotes")
        db.session.add(new_quotes)
        print("Added new quotes")
        db.session.commit()
        print("Returning quotes")
        print(new_quotes)
        print(quote_schema.jsonify(new_quotes))
        return quote_schema.jsonify(new_quotes)
    if request.method == 'GET':
        print("Sending get to quotes")
        all_quotes = Quotes.query.order_by(desc(Quotes.id))
        result = quotes_schema.dump(all_quotes)
        return jsonify(result)

@app.route("/home", methods = ['GET'])
def my_index():
    print("Getting /home")
    return render_template('index.html')

def generator():
    word_vectors = KeyedVectors.load("./giga50.wordvectors", mmap='r')

    quote_file = "./inspa_quotes.csv"
    valid = """ !"$%&'()+,-./:?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"""
    punctuation = """!"$%&()+,-./:?"""

    sents = []
    with open(quote_file, 'r', encoding="unicode_escape") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for quote in (list(row)[0] for row in spamreader):
            if not (280-len(quote)>=0 and 280-len(quote)<=100):
                continue
            quote = quote.lower()
            works = True
            for i in range(len(quote)):
                if quote[i] not in valid:
                    works=False
                    break
            if not works:
                continue
            for p in punctuation:
                quote = quote.replace(p, ' ' + p + ' ')
            quote=quote.replace("i've","ive")
            quote=quote.replace("we've","weve")
            quote=quote.replace("can't","cant")
            quote=quote.replace("won't","wont")
            quote = quote.replace("'", " '")
            quote = quote.replace(" ' ", " ")
            quote = quote.replace("n 't", "  n't")
            quote = quote.replace(" '", " ")
            sents.append([word for word in quote.split(" ") if len(word)>0])
    vecsize = 50
    seq_length = 10
    dataX = []
    dataY = []
    for i in range(len(sents)-1, -1, -1):
        for j in range(len(sents[i])-1, -1, -1):
            if sents[i][j] not in word_vectors:
                del sents[i][j]
    #print(len(sents))
    index=0
    for sentence in sents[:100]:
        for i in range(1, len(sentence)-1):
            index += 1
            #if index % 100000 == 0:
            #    print(index)
            dataX.extend([[0]*vecsize]* max(0, seq_length-i))
            dataX.extend([word_vectors[sentence[j]] for j in range(max(0, i-seq_length),i)])
            dataY.append(word_vectors[sentence[i]])
    n_patterns = index
    #print("Total Patterns: ", n_patterns)
    # reshape X to be [samples, time steps, features]
    X = numpy.reshape(dataX, (n_patterns, seq_length, vecsize))
    y = numpy.reshape(dataY, (n_patterns, vecsize))

    # define the LSTM model
    model = Sequential()
    model.add(Bidirectional(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True)))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.5))
    model.add(Dense(vecsize))
    model.compile(loss='logcosh', optimizer='adam', metrics=['acc'])
    model.built=True
    pattern = X[0]
    x = numpy.reshape(pattern, (1, seq_length, vecsize))
    prediction = model.predict(x, verbose=0)
    filename = "./weights-improvement3-48-0.0748.hdf5"
    model.load_weights(filename)
    # define the checkpoint
    # pick a random seed
    start = numpy.random.randint(0, len(dataX)//seq_length - 1)*10
    pattern = dataX[start:start+10]
    # generate characters
    for i in range(100):
        x = numpy.reshape(numpy.array(pattern).astype('float32'), (1, seq_length, vecsize))
        prediction = model.predict(x, verbose=0)
        result = word_vectors.most_similar(positive=[numpy.reshape(prediction.astype('float32'), (vecsize))],topn=1)[0][0]
        sys.stdout.write(result + " ")
        pattern.append(word_vectors[result])
        pattern = pattern[1:len(pattern)]
    #str1 = "" 
    #for ele in pattern: 
    #    str1 += ele  
    return pattern

if __name__ == '__main__':
    app.run(debug=True)