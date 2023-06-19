import numpy as np
from numpy.linalg import norm
from helper import *
from sklearn.metrics.pairwise import cosine_similarity


def songrecommender(userSongURI, similarSongURI):
    userSongData = []
    for i in userSongURI:
        data=getTrackData(i)
        userSongData.append(data[0][6:-2])
        print(data[0][0])
    print("00000000000000000000000000000000000000000000000000000000000000000000000")
    similarSongData = []
    for i in similarSongURI:
        data = getTrackData(i)
        similarSongData.append(data[0][6:-2])
        print(data[0][0])

    userSongData = np.array(userSongData)
    similarSongData= np.array(similarSongData)
    similarity_matrix = cosine_similarity(userSongData, similarSongData)
    top_values = (-similarity_matrix).argsort(axis=None)[:(len(userSongURI)*len(similarSongURI))]
    top_indices = np.unravel_index(top_values, similarity_matrix.shape)

    recommededSongIndices=[]
    for i in top_indices[1]:
        if i in recommededSongIndices:
            continue
        else:
            recommededSongIndices.append(i)
    top_song_uri=[similarSongURI[i] for i in recommededSongIndices]

    return top_song_uri[0:15]


    