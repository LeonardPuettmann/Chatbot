#importing the libraries
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM , Dense,GlobalMaxPooling1D,Flatten
from tensorflow.keras.models import Model

# importing the dataset
with open('C:\\Users\\leopu\\OneDrive\\Programming\\Python\\Natural Language Processing\\SWD Chatbot\\intent.json') as content:
    data_raw = json.load(content)

# getting all the data to lists
tags = []
inputs = []
responses = {}

for intent in data_raw['intents']:
    responses[intent['tag']] = intent['responses']
    for lines in intent['inputs']:
        inputs.append(lines)
        tags.append(intent['tag'])

# convert do dataframe
data = pd.DataFrame({"inputs" : inputs,
                    "tags": tags})

# removing punctuations 
import string 
data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))

# tokenize the data
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer =  Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])

# apply padding
from tensorflow.keras.preprocessing.sequence import pad_sequences
x_train = pad_sequences(train)

# Encoding the outputs 
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

# input length
input_shape = x_train.shape[1]
print(input_shape)

# define vocab
vocabulary = len(tokenizer.word_index)
print('Number of unique words: ', vocabulary)

# output length
output_lenght = le.classes_.shape[0]
print("Output length: ", output_lenght)

# Creating the model
inp = Input(shape=(input_shape, ))
lay = Embedding(vocabulary+1, 10)(inp)
lay = LSTM(10, return_sequences=True)(lay)
lay = Flatten()(lay)
lay = Dense(output_lenght, activation='softmax')(lay)
model = Model(inp, lay)

# compiling the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# training the model
hist = model.fit(x_train, y_train, epochs=400)

# save the model
model.save('chatbot_adv_model.h5', hist)

#chatting
import random
while True:
  texts_p = []
  prediction_input = input('Du : ')
  #removing punctuation and converting to lowercase
  prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
  prediction_input = ''.join(prediction_input)
  texts_p.append(prediction_input)
  #tokenizing and padding
  prediction_input = tokenizer.texts_to_sequences(texts_p)
  prediction_input = np.array(prediction_input).reshape(-1)
  prediction_input = pad_sequences([prediction_input],input_shape)
  #getting output from model
  output = model.predict(prediction_input)
  output = output.argmax()
  #finding the right tag and predicting

  response_tag = le.inverse_transform([output])[0]
  print('Chatbot der Stadtwerke Düsseldorf : ', random.choice(responses[response_tag]))
  print('   ')
    
  if response_tag == "Verabschieden":
   break