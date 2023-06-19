import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
def decision_tree(weather, mood, time):
    weather_code = {
        'CS': 1,
        'C': 2,
        'R': 3,
        'W': 4,
        'M': 3
    }
    time_code = {
        'M': 1,
        'A': 2,
        'E': 3,
        'N': 4,
    }
    mood_code = {
        'Angry': 4,
        'Disgust': 2,
        'Fear': 5,
        'Happy': 1,
        'Neutral': 2,
        'Sad': 3,
        'Surprised': 2
    }

    code_mood = {
        1: 'Happy',
        2: 'Neutral',
        3: 'Sad',
        4: 'Angry',
        5: 'Fear',
    }


    df = pd.read_csv('data/decision_tree_data.csv')
    X = []
    y = []
    for index, row in df.iterrows():
        X.append([row["weather"], row["time"], row["mood"]])
        y.append([row["tag0"], row["tag1"], row["tag2"], row["tag3"]])
    dt = DecisionTreeClassifier()
    dt.fit(X, y)
    final_tag = np.array(dt.predict([[weather_code[weather], time_code[time], mood_code[mood]]])).flatten()
    final_tag = [code_mood[i] for i in final_tag]
    return final_tag


