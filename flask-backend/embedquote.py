from __future__ import print_function
from datetime import datetime
import os
from flask import render_template, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
#from keras.utils import np_utils
# from keras import regularizers
# from keras.models import Sequential, Model
# from keras.layers import Dense, Activation, Dropout, Embedding, Flatten, Bidirectional, Input, LSTM
# from keras.callbacks import EarlyStopping,ModelCheckpoint
# from keras.optimizers import Adam
# from keras.metrics import categorical_accuracy, mean_squared_error, mean_absolute_error, logcosh
# from keras.layers.normalization import BatchNormalization
# from matplotlib import pyplot as plt
# import numpy
# import math
# import random
# import sys
# import os
# import csv
# from gensim.test.utils import common_texts
# from gensim.models import Word2Vec
# from gensim.models import KeyedVectors
# import gensim.downloader
# import sqlite3

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String)
    image = db.Column(db.String)
    text = db.Column(db.String)
    username = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean)
    avatar = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #C reate a function to return a string when we add something
    def __repr__(self):
        return '<displayName %r>' % self.id 

#db.create_all()
#db.session.commit()

@app.route("/home")
def my_index():
    return render_template('index.html')

@app.route("/home", methods = ["POST"])
def posts():
    displayName = request.form["displayName"]
    id = request.form["id"]
    image = request.form["image"]
    text = request.form["text"]
    username = request.form["username"]
    verified = request.form["verified"]
    avatar = request.form["avatar"]
    connection = sqlite3.connect(currentdirectory + "/posts.db")
    print("Opened database successfully")
    cursor = connection.cursor()
    query1 = "INSERT INTO posts VALUES('{displayName}',{id},'{image}','{text}', '{username}',{verified},'{avatar}')".format(displayName = displayName, id = id, image = image, text = text, username = username, verified = verified, avatar = avatar)
    cursor.execute(query1)
    print("Values inserted successfully")
    connection.commit()

@app.route("/resultpage", methods = ["GET"])
def resultpage():
    try:
        if request.method == "GET":
            name = request.args.get("displayName")
            connection = sqlite3.connect(currentdirectory + "/posts.db")
            print("Opened database successfully")
            cursor = connection.cursor()
            query1 = "SELECT elements from posts WHERE displayName = '{displayName}'".format(displayName = name)
            result = cursor.execute(query1)
            result = result.fetchall()[0][0]
            print("Elements selected successfully")
            return render_template("resultpage.html", displayName = result)
    except:
        return render_template("resultpage.html", displayName = "")


@app.route("/predict", methods = ['POST'])
def generator():
    word_vectors = KeyedVectors.load("./giga.wordvectors", mmap='r')

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
    prediction_text = request.form.get("predict", "")
    return jsonify(predict=pattern)
    #return render_template('index.html', prediction_text=pattern)
    #print ("\nDone.")

@app.route("/predict-api", methods=['POST'])
def predict_api():
    #data = request.get_json(force=True)
    prediction = generator()
    return jsonify(prediction)

app.run(debug=True)
