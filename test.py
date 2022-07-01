# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:49:32 2022

@author: safa
"""

import cv2 
import face_recognition
import numpy as np

ang=face_recognition.load_image_file('test_image/ang_jolie.jpg')
ang=cv2.cvtColor(ang, cv2.COLOR_BGR2RGB)
test=face_recognition.load_image_file('test_image/test1.jpg')
test=cv2.cvtColor(test, cv2.COLOR_BGR2RGB)

face_loc=face_recognition.face_locations(ang)[0]
encod=face_recognition.face_encodings(ang)[0]
cv2.rectangle(ang, (face_loc[3],face_loc[0]), (face_loc[1],face_loc[2]), (255,0,255),2)


loc=face_recognition.face_locations(test)[0]
cod=face_recognition.face_encodings(test)[0]
cv2.rectangle(test, (loc[3],loc[0]), (loc[1],loc[2]), (255,0,255),2)

result=face_recognition.compare_faces([encod], cod)
faceDist=face_recognition.face_distance([encod], cod)
print('are the match : ',result,' ',faceDist)
cv2.putText(test,f'{result} {round(faceDist,2)}', (50,50), cv2.FONT_HERSHEY_COMPLEX,2, (0,0,255),2)


cv2.imshow('angolina',ang)
cv2.imshow('test',test)
cv2.waitKey(0)
