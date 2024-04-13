import os
import pickle
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("faceattendancerealtime-9e7bd-firebase-adminsdk-orspe-ef6f5c208f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-9e7bd-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-9e7bd.appspot.com/Images"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

imgBackground = cv2.imread('Resources/background.png')

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

studentInfo = {}  # Initialize studentInfo as an empty dictionary
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
font_color = (0, 0, 0)
font_thickness = 2
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162: 162 + 480, 55: 55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                print("Known Face Detected")
                print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    detected_name = studentInfo.get('name', 'Unknown')

                    # Display the name on the image
                    cv2.putText(imgBackground, f"Name: {detected_name}", (x1, y1 - 10), font, font_scale,
                                font_color,font_thickness)

                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # blob = bucket.get_blob(f'Images/{id}.png')
                # array = np.frombuffer(blob.download_as_string(), np.uint8)
                # imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update data of attendance
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if 10 < counter < 20:
            modeType = 2

        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if counter <= 10:
            cv2.putText(imgBackground, str(studentInfo.get('total_attendance', 0)), (861, 125),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            cv2.putText(imgBackground, str(studentInfo.get('major', '')), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentInfo.get('standing', '')), (910, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo.get('year', '')), (1025, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo.get('starting_year', '')), (1125, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            (w, h), _ = cv2.getTextSize(studentInfo.get('name', ''), cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414 - w) // 2
            cv2.putText(imgBackground, str(studentInfo.get('name', '')), (808 + offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

            # ... (the rest of your code)
        # imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
        counter += 1
        if counter >= 20:
            counter = 0
            modeType = 0
            studentInfo = []
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)