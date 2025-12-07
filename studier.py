import tensorflow
from tensorflow import keras
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import os
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime
import socket

import requests


face_classifier = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
classifier =load_model(r'./model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

# Define counter for categories and extra label variable
emotion_counter = 0
prev_label = ""


def on_connect(client, userdata, flags, rc):
    """Notify of successful connection"""

    print("Connected to server (i.e., broker) with result code "+str(rc))

#create a client object
client = mqtt.Client()

#attach the on_connect() callback function defined above to the mqtt client
client.on_connect = on_connect

client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

client.loop_start()
sleep(1)

# Define topic to send to
topic="vagutier_ee250_project"

# Sends message to MQTT topic
def send_emotion(emotion):
    client.publish(topic, f"{emotion}")

# Most of the code in the while loop is derived from the cited github repo
# New additions are labeled with comments
while True:
    sleep(0.1)
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]

            # Print current emotion and track for consecutive frames of the same emotion
            print(f"Current emotion is: {label}")
            if label == prev_label: # Check for consecutive frame and increment counter if true
                emotion_counter = emotion_counter + 1
            else: # Reset counter on new emotion
                emotion_counter = 0
            
            # After 5 consecutive frames, send an MQTT message and reset counter
            if (emotion_counter == 5):
                send_emotion(label)
                emotion_counter = 0

            prev_label = label # Update label to check on next frame

            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()