from helper import *
import json

#Script to obtain data 
import numpy as np 
import pandas as pd 

#Libraries to create the multiclass model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
#Import tensorflow and disable the v2 behavior and eager mode
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

#Library to validate the model
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.pipeline import Pipeline

import warnings

warnings.filterwarnings("ignore")


def songprofile():
    df = pd.read_csv("data/song_profile_data.csv")

    col_features = df.columns[6:-3]
    X= MinMaxScaler().fit_transform(df[col_features])
    X2 = np.array(df[col_features])
    Y = df['mood']

    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_y = encoder.transform(Y)


    #Convert to  dummy (Not necessary in my case)
    dummy_y = np_utils.to_categorical(encoded_y)

    X_train,X_test,Y_train,Y_test = train_test_split(X,encoded_y,test_size=0.5,random_state=15)

    target = pd.DataFrame({'mood':df['mood'].tolist(),'encode':encoded_y}).drop_duplicates().sort_values(['encode'],ascending=True)

    def base_model():
        #Create the model
        model = Sequential()
        #Add 1 layer with 8 nodes,input of 4 dim with relu function
        model.add(Dense(15,input_dim=10,activation='relu'))
        #Add 1 layer with output 3 and softmax function
        model.add(Dense(5,activation='softmax'))
        #Compile the model using sigmoid loss function and adam optim
        model.compile(loss='categorical_crossentropy',optimizer='adam',
                    metrics=['accuracy'])
        return model

    #Configure the model
    estimator = KerasClassifier(build_fn=base_model,epochs=300,batch_size=20,verbose=0)

    kfold = KFold(n_splits=5,shuffle=True)
    results = cross_val_score(estimator,X,encoded_y,cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100,results.std()*100))

    estimator.fit(X_train,Y_train)
    y_preds = estimator.predict(X_test)

    def predict_mood(id_song):
        #Join the model and the scaler in a Pipeline
        pip = Pipeline([('minmaxscaler',MinMaxScaler()),('keras',KerasClassifier(build_fn=base_model,epochs=300,
                                                                                batch_size=30,verbose=0))])
        #Fit the Pipeline
        pip.fit(X2,encoded_y)

        #Obtain the features of the song
        preds = getTrackData(id_song)
        #Pre-process the features to input the Model
        preds_features = np.array(preds[0][6:-2]).reshape(-1,1).T

        #Predict the features of the song
        results = pip.predict(preds_features)

        mood = np.array(target['mood'][target['encode']==int(results)])

        return mood[0]

    user=input('Enter user id: ')
    userTopArt=getuserTopArtist(user)
    userTopArtURI=[]
    for i in userTopArt:
        userTopArtURI.append(getArtistURI(i))

    ArtistTopSongURI=[]

    for i in userTopArtURI:
        ArtistTopSongURI.append(getArtistsTopTrack(i))

    userSongProfile={
        'Angry': [],
        'Happy': [],
        'Neutral': [],
        'Sad': [],
        'Fear': []
    }

    userTopSongURI=[]

    for i in ArtistTopSongURI:
        for j in i:
            userTopSongURI.append(j)
            userSongProfile[predict_mood(j)].append(j)
            print(j)
    with open('userSongProfile.json', "w") as file:
        json.dump(userSongProfile,file)
        file.close()
    with open('userTopSongURI.json', "w") as file:
        json.dump(userTopSongURI, file)
        file.close()
    return userSongProfile, userTopSongURI

