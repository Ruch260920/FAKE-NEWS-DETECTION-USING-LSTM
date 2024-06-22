# -*- coding: utf-8 -*-
"""Aditya_English_Lstm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1URc6jG_vGdvqe8ac9cVPN6i52wiSADAc

# Fake news detection

##Importing Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import re
from wordcloud import WordCloud
import pandas
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Conv1D, MaxPool1D
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

"""## Exploring Fake News

##Reading dataset
"""

fake = pd.read_csv('Fake.csv')

fake.shape

fake.head()

fake.columns

fake['subject'].value_counts()

plt.figure(figsize=(10, 6))
sns.countplot(x ='subject',data=fake)

"""##WordCloud for Fake Dataset"""

text = ' '.join(fake['text'].tolist())

' '.join(['this', 'is', 'a', 'data'])

from wordcloud import WordCloud
wordcloud = WordCloud(width=1920, height=1080).generate(text)
plt.imshow(wordcloud)
fig = plt.figure(figsize=(10,10))
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

"""##Exploring Real News"""

real = pd.read_csv('True.csv')

text = ' '.join(real['text'].tolist())

from wordcloud import WordCloud
wordcloud = WordCloud(width=1920, height=1080).generate(text)
plt.imshow(wordcloud)
fig = plt.figure(figsize=(5,5))
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

"""Cleaning the dataset"""

real.sample(5)

unknown_publishers = []
for index, row in enumerate(real.text.values):
  try:
    record = row.split('-', maxsplit=1)
    record[1]

    assert(len(record[0])<120)
  except:
    unknown_publishers.append(index)

len(unknown_publishers)

real.iloc[unknown_publishers].text

real.iloc[8970]

real = real.drop(8970, axis=0)

publisher = []
tmp_text = []

for index, row in enumerate(real.text.values):
  if index in unknown_publishers:
    tmp_text.append(row)
    publisher.append('Unknown')

  else:
    record = row.split('-', maxsplit=1)
    publisher.append(record[0].strip())
    tmp_text.append(record[1].strip())

tmp_text.append(row)
publisher.append('Unknown')

real.head()

real.shape

empty_fake_index = [ index for index, text in enumerate (fake.text.tolist()) if str(text).strip()==""]

fake.iloc[empty_fake_index]

real['text'] = real['title'] + " " + real['text']
fake['text'] = fake['title'] + " " + fake['text']

real['text'] = real['text'].apply(lambda x: str(x).lower())
fake['text'] = fake['text'].apply(lambda x: str(x).lower())

"""### Pre-processing Text"""

real['class'] = 1
fake['class'] = 0

real.columns

real = real[['text', 'class']]

fake = fake[['text', 'class']]

data = real.append(fake, ignore_index=True)

data.sample(5)

!pip install spacy==2.2.3
!python -m spacy download en_core_web_sm
!pip install beautifulsoup4==4.9.1
!pip install textblob==0.15.3
!pip install git+https://github.com/laxmimerit/preprocess_kgptalkie.git --upgrade --force-reinstall

import preprocess_kgptalkie as ps

"""##Data Cleaning and Preparation"""

ps.remove_special_chars('this , . @ # is & * great ')

data['text'] = data['text'].apply(lambda x: ps.remove_special_chars(x))

data.head()

import gensim

y = data['class'].values

X = [d.split() for d in data['text'].tolist()]

type(X[0])

type(X[0])

DIM = 100
w2v_model = gensim.models.Word2Vec(sentences=X, size=DIM, window=10, min_count=1)

len(w2v_model.wv.vocab)

w2v_model.wv.vocab

w2v_model.wv.most_similar('india')

w2v_model.wv['obama']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

X = tokenizer.texts_to_sequences(X)

tokenizer.word_index

tokenizer.word_index

plt.hist([len(x) for x in X], bins = 700)
plt.show

nos = np.array([len(x) for x in X])
len(nos[nos>1000])

maxlen = 1000
X = pad_sequences(X,maxlen=maxlen)

len(X[20])

vocab_size = len(tokenizer.word_index) + 1
vocab = tokenizer.word_index

def get_weight_matrix(model):
  weight_matrix = np.zeros((vocab_size, DIM))

  for word, i in vocab.items():
    weight_matrix[i] = model.wv[word]

  return weight_matrix

embedding_vectors = get_weight_matrix(w2v_model)

embedding_vectors.shape

model = Sequential()
model.add(Embedding(vocab_size, output_dim=DIM, weights = [embedding_vectors], input_length=maxlen, trainable=False))
model.add(LSTM(units=64))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

"""#Training of Model"""

model.summary()

X_train, X_test, y_train, y_test = train_test_split(X,y)

history = model.fit(X_train,y_train, epochs =10, validation_data=(X_test,y_test))

history_dict = history.history

acc = history_dict['acc']
val_acc = history_dict['val_acc']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = history.epoch

plt.figure(figsize=(12,9))
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss', size=20)
plt.xlabel('Epochs', size=20)
plt.ylabel('Loss', size=20)
plt.legend(prop={'size': 20})
plt.savefig('Training and Validation Loss BLSTM.jpg',bbox_inches = 'tight',transparent=True)
plt.show()

plt.figure(figsize=(12,9))
plt.plot(epochs, acc, 'g', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy', size=20)
plt.xlabel('Epochs', size=20)
plt.ylabel('Accuracy', size=20)
plt.legend(prop={'size': 20})
plt.ylim((0.90,1.10))
plt.savefig('Training and Validation Accuracy BLSTM.jpg',bbox_inches = 'tight',transparent=True)
plt.show()

y_pred = (model.predict(X_test) >=0.5).astype(int)

accuracy_score(y_test, y_pred)

print(classification_report(y_test, y_pred))

plt.figure(figsize=(10,10))
plt.scatter(y_test, y_pred, c='crimson')
plt.yscale('log')
plt.xscale('log')

p1 = max(max(y_pred), max(y_test))
p2 = min(min(y_pred), min(y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.show()

x = ['this is a news']

X_test

len(tokenizer.texts_to_matrix(x)[0])

x = ['this is a news']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)

(model.predict(x) >=0.5).astype(int)

"""#Testing Data"""

x = ['Lockdowns during the pandemic forced migrant workers across India to return home. Here’s how migrants from East UP coped with the consequences, and how the government, nonprofits, and funders can support them.']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)
(model.predict(x) >=0.5).astype(int)

x = ['(Reuters)Pterosaurs ruled the skies during the age of the dinosaurs, but scientists have long debated if they actually had feathers. Now we know. Not only did these flying reptiles have feathers, but they could actually control the color of those feathers on a cellular level to create multicolor plumage in a way similar to modern birds, new research has revealed.']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)
(model.predict(x) >=0.5).astype(int)

x = ['India reported 2,927 new coronavirus cases today, bringing the total number of infections to 4,30,65,496. According to the Union Health Ministry, the active cases increased to 16,279,The country also reported 32 deaths in the last 24 hours, taking the total number of covid-related fatalities to 5,23,654.The active cases comprise 0.04 per cent of the total infections, while the national COVID-19 recovery rate was recorded as 98.75 per cent, the ministry said. An increase of 643 cases has been recorded in the active COVID-19 caseload in a span of 24 hours.']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)
(model.predict(x) >=0.5).astype(int)

x = ['Russia tests new intercontinental ballistic missile Reuters | Updated: Apr 20, 2022, 20:50 IST Russia said on Wednesday it had test-launched its Sarmat intercontinental ballistic missile, a new addition to its nuclear arsenal which President Vladimir Putin said would give Moscows enemies something to think about. Putin was shown on television being told by the military that the missile had been launched from Plesetsk in the countrys northwest and hit targets in the Kamchatka peninsula in the far east.']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)
(model.predict(x) >=0.5).astype(int)