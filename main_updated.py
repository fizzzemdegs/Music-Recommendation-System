from faceopencv import mood
from weathercode import *
from songprofile import *
import json
import os
from helper import *
from recomender import *
from createplaylist import *
from timecode import *
from decisiontree import *
import warnings
import webbrowser

warnings.filterwarnings("ignore")
mood_tag = mood()
print('Facial Mood Detected: ', mood_tag)
weather_tag = weather_tag()
time_tag = time_code_generator()

final_tag = list(set(decision_tree(weather_tag, mood_tag, time_tag)))
print('Final List of Tag with Priority: ', final_tag)

userSongProfile = {}
userTopSongURI = []
if os.path.exists('userSongProfile.json'):
    with open('userSongProfile.json', "r") as file:
        userSongProfile = json.load(file)
        file.close()
    with open('userTopSongURI.json', "r") as file:
        userTopSongURI = json.load(file)
        file.close()
else:
    userSongProfile, userTopSongURI = songprofile()

userMoodSongs = userSongProfile[mood_tag][0:5]
recommendedSong = getSimilarTrack(userMoodSongs)
playlist_URI = createplaylist(recommendedSong, mood_tag)
print('///Your Playlist has been created///')
webbrowser.open('https://open.spotify.com/playlist/'+playlist_URI)