import requests
import geocoder
from pyowm import OWM
from datetime import datetime
import requests
from spotifytoken import getSpotifyToken
from lastfmkey import *


def getmetadata():
    now = datetime.now()
    time_formatted = now.strftime("%H:%M:%S")

    ip_address = geocoder.ip('me')
    lat, lng = ip_address.latlng
    owm = OWM('8aa4f173bbbb157abbce710e59499f7c')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lng)
    weather = observation.weather.detailed_status

    url = f"https://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&appid=6b0e333ea9e514c03c18d23ecf227efa&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data["main"]["temp"]

    return [ip_address.city, weather, time_formatted, temperature]

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

