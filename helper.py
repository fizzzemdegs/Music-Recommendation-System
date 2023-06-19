import requests
from spotifytoken import getSpotifyToken
from lastfmkey import *

def getTrackTags(artist,track):
    headers = {
        'user-agent': LASTFM_USER_AGENT
    }
    payload = {
        'api_key': LASTFM_API_KEY,
        'method': 'track.getInfo',
        'artist': artist,
        'track': track,
        'format': 'json',
        'user': 'Fizz'
    }
    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    data=r.json()
    track_info={'name': data['track']['name'], 'tag':[i['name'] for i in data['track']['toptags']['tag']] }
    return track_info

def getuserTopTracks(user):
    headers = {
        'user-agent': LASTFM_USER_AGENT
    }

    payload = {
        'api_key': LASTFM_API_KEY,
        'method': 'user.getTopTracks',
        'format': 'json',
        'user': user,
    }
    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    data=r.json()
    song=[i['name'] for i in data['toptracks']['track']]
    return song

def getTrackData(id):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'ids':id
    }
    r = requests.get('https://api.spotify.com/v1/audio-features', headers=headers, params=payload)
    data=r.json()

    acousticness = data['audio_features'][0]['acousticness']
    danceability = data['audio_features'][0]['danceability']
    energy = data['audio_features'][0]['energy']
    instrumentalness = data['audio_features'][0]['instrumentalness']
    liveness = data['audio_features'][0]['liveness']
    valence = data['audio_features'][0]['valence']
    loudness = data['audio_features'][0]['loudness']
    speechiness = data['audio_features'][0]['speechiness']
    tempo = data['audio_features'][0]['tempo']
    key = data['audio_features'][0]['key']
    time_signature = data['audio_features'][0]['time_signature']

    r = requests.get('https://api.spotify.com/v1/tracks', headers=headers, params=payload)
    data=r.json()
    
    name = data['tracks'][0]['name']
    album = data['tracks'][0]['album']['name']
    artist = data['tracks'][0]['artists'][0]['name']
    release_date = data['tracks'][0]['album']['release_date']
    length = data['tracks'][0]['duration_ms']
    popularity = data['tracks'][0]['popularity']
    ids =  id

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
            energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name','album','artist','id','release_date','popularity','length','danceability','acousticness','energy','instrumentalness',
                'liveness','valence','loudness','speechiness','tempo','key','time_signature']
    return track,columns

def getSongURI(query):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'q':query,
        'type':'track',
        'limit':'1',
        'offset':'0'
    }
    r = requests.get('https://api.spotify.com/v1/search', headers=headers, params=payload)
    data=r.json()
    return data['tracks']['items'][0]['id']

def getArtistURI(query):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'q':query,
        'type':'artist',
        'limit':'1',
        'offset':'0'
    }

    r = requests.get('https://api.spotify.com/v1/search', headers=headers, params=payload)
    data=r.json()
    return data['artists']['items'][0]['id']

def getArtistsTopTrack(ids):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'market':'es'
    }

    r = requests.get('https://api.spotify.com/v1/artists/'+ids+'/top-tracks', headers=headers, params=payload)
    data=r.json()
    topTrackURI=[i['id'] for i in data['tracks']]
    return topTrackURI[0:10]

def getuserTopArtist(user):
    headers = {
        'user-agent': LASTFM_USER_AGENT
    }

    payload = {
        'api_key': LASTFM_API_KEY,
        'method': 'user.getTopArtists',
        'format': 'json',
        'user': user,
    }
    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    data=r.json()
    userTopArtist=[data['topartists']['artist'][i]['name'] for i in range(5)]
    return userTopArtist

def getTrackandArtistURI(songURI):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'ids':songURI,
    }
    r = requests.get('https://api.spotify.com/v1/tracks', headers=headers, params=payload)
    data=r.json()
    artistURI=data['tracks'][0]['artists'][0]['id']
    

    return songURI,artistURI

def getSimilarTrack(songURI,artistURI):
    headers = {
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'limit': 5,
        'market': 'ES',
        'seed_artists': artistURI,
        'seed_tracks': songURI
    }
    r = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=payload)
    data=r.json()
    similarTrackURI=[]
    for i in range(3):
        similarTrackURI.append(data['tracks'][i]['id'])
    return similarTrackURI

def getSimilarTrack(songURI):
    headers = {
        'Authorization': 'Bearer ' + getSpotifyToken()
    }

    payload ={
        'limit': 15,
        'market': 'ES',
        'seed_tracks': ','.join(songURI)
    }
    r = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=payload)
    data = r.json()
    similarTrackURI = []
    for i in range(15):
        similarTrackURI.append(data['tracks'][i]['id'])
    return similarTrackURI