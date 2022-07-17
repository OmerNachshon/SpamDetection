from wordcloud import WordCloud
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.model_selection import train_test_split
import neattext.functions as nfx
from sklearn.metrics import classification_report
import keras
from keras.layers import Embedding,Dense,LSTM,Bidirectional,GlobalMaxPooling1D,InputLayer,Dropout
from keras.callbacks import EarlyStopping,ReduceLROnPlateau
from keras.models import Sequential
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm
import seaborn as sns
import pickle
import warnings
warnings.filterwarnings('ignore')
def clean_text(text):
    text_length=[]
    cleaned_text=[]
    for sent in tqdm(text):
        sent=sent.lower()
        sent=nfx.remove_special_characters(sent)
        sent=nfx.remove_stopwords(sent)
#         sent=nfx.remove_shortwords(sent)
        text_length.append(len(sent.split()))
        cleaned_text.append(sent)
    return cleaned_text,text_length
#
# data=pd.read_csv('Suicide_Detection.csv')
# data.head()
# train_data,test_data=train_test_split(data,test_size=0.2,random_state=10)
# cleaned_train_text,train_text_length=clean_text(train_data.text)
# cleaned_test_text,test_text_length=clean_text(test_data.text)
# tokenizer=Tokenizer()
# tokenizer.fit_on_texts(cleaned_train_text)
# with open('tokenizer.pkl', 'wb') as handle:
#     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# word_freq=pd.DataFrame(tokenizer.word_counts.items(),columns=['word','count']).sort_values(by='count',ascending=False)
# train_text_seq=tokenizer.texts_to_sequences(cleaned_train_text)
# train_text_pad=pad_sequences(train_text_seq,maxlen=40)
#
#
# test_text_seq=tokenizer.texts_to_sequences(cleaned_test_text)
# test_text_pad=pad_sequences(test_text_seq,maxlen=40)
# lbl_target=LabelEncoder()
# train_output=lbl_target.fit_transform(train_data['class'])
# test_output=lbl_target.transform(test_data['class'])
#
# # glove_embedding={}
# with open('input/glove.840B.300d.pkl', 'rb') as fp:
#     glove_embedding = pickle.load(fp)
# v=len(tokenizer.word_index)
#
# embedding_matrix=np.zeros((v+1,300), dtype=float)
# for word,idx in tokenizer.word_index.items():
#     embedding_vector=glove_embedding.get(word)
#     if embedding_vector is not None:
#         embedding_matrix[idx]=embedding_vector
# early_stop=EarlyStopping(patience=5)
# reducelr=ReduceLROnPlateau(patience=3)
#
# model=Sequential()
# input=InputLayer(input_shape=(40,))
# model.add(input)
# model.add(Embedding(v+1,300,weights=[embedding_matrix],trainable=False))
# model.add(LSTM(20,return_sequences=True))
# model.add(GlobalMaxPooling1D())
# #     model.add(Dropout(0.3))
# model.add(Dense(256,activation='relu'))
# #     model.add(Dropout(0.2))
# model.add(Dense(1,activation='sigmoid'))
# model.compile(optimizer=keras.optimizers.SGD(0.1,momentum=0.09),loss='binary_crossentropy',metrics=['accuracy'])
# r=model.fit(train_text_pad,train_output,validation_data=(test_text_pad,test_output),
#             epochs=10,batch_size=256,callbacks=[early_stop,reducelr])
#
# with open('model.pkl', 'wb') as handle:
#     pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
#

