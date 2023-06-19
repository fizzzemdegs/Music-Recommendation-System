import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from helper import *
import json



def songprofile():
    df = pd.read_csv('data/song_profile_data.csv')

    df = pd.get_dummies(df, columns=['mood'])

    code_mood = {
            2: 'Happy',
            3: 'Neutral',
            4: 'Sad',
            0: 'Angry',
            1: 'Fear',
        }

    X = []
    y = []
    for index, row in df.iterrows():
        X.append([
                    row['danceability'],
                    row['acousticness'],
                    row['energy'],
                    row['instrumentalness'],
                    row['liveness'],
                    row['valence'],
                    row['loudness'],
                    row['speechiness'],
                    row['tempo'],
                    row['key']
                 ])
        y.append([
                    row['mood_Angry'],
                    row['mood_Fear'],
                    row['mood_Happy'],
                    row['mood_Neutral'],
                    row['mood_Sad']
                 ])

    dt = DecisionTreeClassifier()
    dt.fit(X, y)
    def predict_mood(URI):
        data = getTrackData(URI)[0]
        final_tag = np.array(dt.predict([data[6:-2]])).flatten()
        print(final_tag)
        loc=np.where(final_tag==1)[0][0]
        print(loc)
        return code_mood[loc]

    user = input('Enter user id: ')
    userTopArt = getuserTopArtist(user)
    userTopArtURI = []
    for i in userTopArt:
        userTopArtURI.append(getArtistURI(i))

    ArtistTopSongURI = []

    for i in userTopArtURI:
        ArtistTopSongURI.append(getArtistsTopTrack(i))

    userSongProfile = {
        'Angry': [],
        'Happy': [],
        'Neutral': [],
        'Sad': [],
        'Fear': []
    }

    userTopSongURI = []

    for i in ArtistTopSongURI:
        for j in i:
            userTopSongURI.append(j)
            userSongProfile[predict_mood(j)].append(j)
            print(j)
    with open('userSongProfile.json', "w") as file:
        json.dump(userSongProfile, file)
        file.close()
    with open('userTopSongURI.json', "w") as file:
        json.dump(userTopSongURI, file)
        file.close()
    return userSongProfile, userTopSongURI


