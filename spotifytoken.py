import requests
import base64
import json




def getSpotifyToken():
    clientId = '######'
    clientSecret = '######'
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']

    return token
