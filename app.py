# importing libraries
from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

app = Flask(__name__)
@app.route('/')

def home():
    return render_template("home.html")

@app.route("/predict", methods = ["POST"])

def predict():
    # loading the dataset
    data = pd.read_csv("language_detection.csv")
    y = data["Language"]

    # label encoding
    y = le.fit_transform(y)

    #loading the model and cv
    model = pickle.load(open("model.pkl", "rb"))
    cv = pickle.load(open("transform.pkl", "rb"))

    if request.method == "POST":
        # taking the input
        text = request.form["text"]
        # preprocessing the text
        text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', '', text)
        text = re.sub(r'[[]]', '', text)
        text = text.lower()
        dat = [text]
        # creating the vector
        vect = cv.transform(dat).toarray()
        # prediction
        my_pred = model.predict(vect)
        my_pred = le.inverse_transform(my_pred)

    return render_template("home.html", pred=" The above text is in {}".format(my_pred[0]))



if __name__ =="__main__":
    port = int(os.environ.get('PORT', 5000))  # Get port from environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
