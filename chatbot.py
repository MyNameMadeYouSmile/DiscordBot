import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import json
import random

with open("intents.json") as file:
  chatdata = json.load(file)
  
words = []
labels = []
docs_x = []
docs_y = []

for intent in chatdata["intents"]:
  for pattern in intent["patterns"]:
    wrds = nltk.word_tokenize(pattern)
    words.extend(wrds)
    docs_x.append(pattern)
    docx_y.append(intent["tag"]
    
  if intent["tag"] not in labels:
    labels.append(intent["tag"])
    
words = [stemmer.stem(w.lower()) for w in words]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(classes))]

for doc in docs_x:
