from __future__ import print_function
from datetime import datetime
from flask import render_template, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import Column, ForeignKey, Integer, String, desc
import os

from keras.utils import np_utils
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
import os
import csv
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader
import sqlite3

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask("__name__")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quotes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create db model
class Quotes(db.Model):
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
def api():
    tweet = generator()
    if request.method == 'POST':
        id = Quotes.query.order_by('id').all()[-1].id + 1
        category = 'quotes' 
        text = tweet 
        new_quotes = Quotes(id, category, text)
        db.session.add(new_quotes)
        db.session.commit()
        print(new_quotes)
        return quote_schema.jsonify(new_quotes)
    elif request.method == 'GET':
        all_quotes = Quotes.query.order_by(desc(Quotes.id))
        result = quotes_schema.dump(all_quotes)
        print(result)
        return jsonify(result)
    else:
        return render_template('index.html')

@app.route("/home")
def my_index():
    return render_template('index.html')

def generator():
    word_vectors = KeyedVectors.load("./giga50.wordvectors", mmap='r')

    quote_file = "./inspa_quotes.csv"
    # quote_file = "inspa_quotes.csv"
    valid = """ !"$%&'()+,-./:?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n"""
    punctuation = """!"$%&()+,-./:?"""
    # tofind = [" haven't ", " don't ", " one's ", " what's ", " can't ", " 'idiot "]
    # toreplace = [" have n't ", " do n't ", " one 's ", " what 's ", " cant ", " idiot "]

    sents = []
    with open(quote_file, 'r', encoding="unicode_escape") as csvfile:
        #csvfile = ''.join(c for c in csvfile if c not in ',"')
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for quote in (list(row)[0] for row in spamreader):
            quote = quote.lower()
            if not (280-len(quote)>=0 and 280-len(quote)<=100):
                continue
            works = True
            for i in range(len(quote)):
                if quote[i] not in valid:
                    works=False
                    break
            if not works:
                continue
            for p in punctuation:
                quote = quote.replace(p, ' ' + p + ' ')
            quote = quote.replace("'", " '")
            quote = quote.replace(" ' ", " ")
            quote = quote.replace("n 't", "  n't")
            quote = quote.replace(" '", " ")
            sents.append([word for word in quote.split(" ") if len(word)>0])
    vecsize = 100
    # model.save("word2vec.model")
    # Store just the words + their trained embeddings.
    # word_vectors.save("word2vec.wordvectors")
    # Load back with memory-mapping = read-only, shared across processes.
    # wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')

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
    model.add(Bidirectional(LSTM(256)))
    model.add(Dropout(0.5))
    model.add(Dense(vecsize))
    model.compile(loss='logcosh', optimizer='adam', metrics=['acc'])
    model.built=True
    pattern = X[0]
    x = numpy.reshape(pattern, (1, seq_length, vecsize))
    prediction = model.predict(x, verbose=0)
    filename = "./weights-improvement-20-0.0405.hdf5"
    model.load_weights(filename)
    # define the checkpoint

    # pick a random seed
    start = numpy.random.randint(0, len(dataX)//seq_length - 1)*10
    pattern = dataX[start:start+10]
    #print( "Seed:")
    #print ("\"", ' '.join([word_vectors.most_similar(positive=[value],topn=1)[0][0] for value in pattern]), "\"")
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
    #return render_template('index.html', prediction_text=pattern)
    #print ("\nDone.")

if __name__ == '__main__':
    app.run(debug=True)
