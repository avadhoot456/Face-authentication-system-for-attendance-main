import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("faceattendancerealtime-9e7bd-firebase-adminsdk-orspe-ef6f5c208f.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-9e7bd-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-9e7bd.appspot.com"
})


ref = db.reference('Students')

data = {
    "2213482":
        {
            "name": "Sharv Sankpal",
            "major": "CSF",
            "starting_year": 2023,
            "total_attendance": 8,
            "standing": "R",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },

    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "R",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 3,
            "standing": "I",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 8,
            "standing": "R",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2213461":
        {
            "name": "Ashwin Ghadi",
            "major": "CSF",
            "starting_year": 2023,
            "total_attendance": 8,
            "standing": "R",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
    "2213470":
        {
            "name": "Man Kadu",
            "major": "CSF",
            "starting_year": 2023,
            "total_attendance": 8,
            "standing": "R",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        }
}
for key, value in data.items():
    ref.child(key).set(value)