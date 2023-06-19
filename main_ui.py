from flask import Flask, render_template, Response
import cv2
from newhelper import *
import keras
from tensorflow.keras.models import load_model
from time import sleep
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os
import webbrowser
import json
from createplaylist import *

app = Flask(__name__)
camera = cv2.VideoCapture(1)
face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
classifier = load_model(r'trained_model', compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprised']
def generate_frames():
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    label = emotion_labels[prediction.argmax()]
                    with open('filename.txt', 'w') as f:
                        f.write(label)
                        f.close()
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    info = getmetadata()
    data = {'location': info[0], 'weather': info[1], 'time': info[2], 'temperature': info[3], 'mood': 'Check'}
    return render_template('index.html', data=data)

@app.route('/playlist')
def playlist():
    info = getmetadata()
    mood=''
    with open('filename.txt', 'r') as f:
        # Read the contents of the file using read() method
        mood = f.read()
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
    userMoodSongs = userSongProfile[mood][0:5]
    recommendedSong = getSimilarTrack(userMoodSongs)
    playlist_URI = createplaylist(recommendedSong, mood)
    webbrowser.open('https://open.spotify.com/playlist/'+str(playlist_URI))
    data = {'location': info[0], 'weather': info[1], 'time': info[2], 'temperature': info[3], 'mood': mood}
    return render_template('index.html', data=data)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True,port=12121)
