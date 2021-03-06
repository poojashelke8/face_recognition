import face_recognition
import numpy as np
import cv2
import os
from datetime import datetime

path = 'trainset/trainset/trainset/0001/0001_0000265'
images = []
classNames = []
mylist = os.listdir(path)
print(mylist)

for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDatalist = f.readline()
        namelist = []
        for line in myDatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dstring}')



encodelistknown = findEncodings(images)
print("encoding complete..")

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facecurFrame = face_recognition.face_locations(imgS)
    encodecurframe = face_recognition.face_encodings(imgS,facecurFrame)

    for encodeface,faceloc in  zip(encodecurframe,facecurFrame):
        matches = face_recognition.compare_faces(encodelistknown,encodeface)
        faceDis = face_recognition.face_distance(encodelistknown,encodeface)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            print(name)
            y1,x2,y2,x1 = faceloc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),2)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('webcam',img)
    cv2.waitKey(1)




