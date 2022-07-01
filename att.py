# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 11:08:56 2022

@author: safa
"""

import cv2 
import face_recognition
import numpy as np

import os
from datetime import time
open('attendance.csv', 'a')
path='test_image'
images=[]
classNames=[]
list=os.listdir(path)
print(list)
for l in list:
    img=cv2.imread(f'{path}/{l}')
    images.append(img)
    classNames.append(os.path.splitext(l)[0])
print(classNames)

def findencodeings(images):
    encod_list=[]
    for img in images:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encod=face_recognition.face_encodings(img)[0]
        encod_list.append(encod)
    return encod_list

#def markAttendance(name):
    

encodList=findencodeings(images)
print(len(encodList))

cap=cv2.VideoCapture(0)

while True:
    succes,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurrentFrame=face_recognition.face_locations(imgS)
    encodeCurrentFrame=face_recognition.face_encodings(imgS,faceCurrentFrame)
    for encodeFace,faceLoc in zip(encodeCurrentFrame,faceCurrentFrame):
        #zip cuz same the loop
        matches=face_recognition.compare_faces(encodList, encodeFace)
        faceDis=face_recognition.face_distance(encodList, encodeFace)
        print(faceDis)
        matchIndex=np.argmin(faceDis)
        
        if matches[matchIndex]:
            name=classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1,y1) ,(x2,y2), (0,255,0),2)
            cv2.rectangle(img, (x1,y2-35) ,(x2,y2), (0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow('webcam',img)   
    cv2.waitKey(1)     
       
