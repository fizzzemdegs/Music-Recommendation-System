import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime




def createplaylist(recommendedSongURI, mood_tag):
    # Set up authentication using SpotifyOAuth
    scope = "playlist-modify-public"  # Modify public playlists
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id="a2ed8135191844b383ca1740f5238122",
                                                   client_secret="2b2ab626d82a4d1fb3dad785c4c07221",
                                                   redirect_uri="http://localhost:3000/callback"))

    # Create a new playlist
    playlist_name = 'Playlist @ '+ str(datetime.now().strftime("%H:%M:%S"))
    playlist_description = "A new playlist created accourding to your mood!!!"
    user_id = sp.me()["id"]  # Get current user's ID
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description)

    # Add tracks to the playlist
    head = 'spotify:track:'
    track_uris = []
    for i in recommendedSongURI:
        track_uris.append(head + i)
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
    return playlist["id"]
