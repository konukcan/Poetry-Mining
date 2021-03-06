###Here is the code to extract emotions from sentences in a text.
#Reminder:  the arrays after each sentence score emotions in the following order : joy, fear, sadness, anger, surprise, disgust.


import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
url = 'http://www.gutenberg.org/files/12005/12005-h/12005-h.htm'
import pandas as pd
import numpy as np



file = 'FEEL.csv'
feel_data = pd.read_csv(file)
feely_data = pd.DataFrame(feel_data)
feely_dict = {}

r = requests.get(url)
r.encoding = 'utf-8'
html = r.text


soup = BeautifulSoup(html, features="lxml")
text = soup.get_text()
sentences = text.split(".")

for index, row in feely_data.iterrows():
    feely_dict[row['word']] = list(row[3:10])


sentences_and_scores = []

for sent in sentences:
    array = []
    for mot in sent.split():
        if mot in feely_dict:
           array.append(feely_dict.get(mot))
    sentences_and_scores.append(sent)
    sentences_and_scores.append([sum(i) for i in zip(*array)])

for element in sentences_and_scores[550:600]:
    print("::: \n")
    print(element)
