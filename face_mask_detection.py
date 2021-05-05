# -*- coding: utf-8 -*-
"""technovate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aTD-ew4GwOtjhadsZ06n2xINPLAK9yjh
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random

from google.colab import drive
drive.mount('/content/gdrive/')

DIRECTORY = '/content/gdrive/My Drive/Robotics club- Purwanchal Campus Dharan/projects/facemask dataset'
CATEGORIES = ['with mask','without mask']

data=[]

for category in CATEGORIES:
    path = os.path.join(DIRECTORY,category)
    for img in os.listdir(path):
        img_path = os.path.join(path,img)
        label = CATEGORIES.index(category)
        array = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(array,(60,60))
        data.append([new_array,label])

random.shuffle(data)

x = []
y = []
for feature,label in (data):
    x.append(feature)
    y.append(label)

x = np.array(x)
y = np.array(y)

x = x/255
x = x.reshape(-1,60,60,1)

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

model = Sequential()
 
# model.add(Conv2D(64, (3,3), activation = 'relu'))
# model.add(MaxPooling2D((2,2)))
 
model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))
 
model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))
 
model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D((2,2)))
 
model.add(Flatten())
 
model.add(Dense(128, input_shape = (60,60,1), activation = 'relu'))
 
model.add(Dense(2, activation = 'softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x,y,validation_split=0.1,epochs=10)

# our_model = tf.keras.models.load_model('/content/gdrive/My Drive/Robotics club- Purwanchal Campus Dharan/projects/mask_detector.model')

face_classifier = cv2.CascadeClassifier('/content/gdrive/My Drive/Robotics club- Purwanchal Campus Dharan/projects/haarcascade_frontalface_alt.xml')
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image

from google.colab.patches import cv2_imshow
frame = cv2.imread('/content/gdrive/My Drive/aadesh/without_mask.jpg')
frame = cv2.resize(frame,(400,500))
labels = []
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
faces = face_classifier.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(60,60),interpolation=cv2.INTER_AREA)
    # rect,face,image = face_detector(frame)


        roi = roi_gray.astype('float')/255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi,axis=0)
        print(roi.shape)

        # make a prediction on the ROI, then lookup the class

        preds = model.predict(roi)[0]
        label=CATEGORIES[preds.argmax()]
        label_position = (x,y)
        cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
        print(label)
        print(label)
     
cv2_imshow(frame)

