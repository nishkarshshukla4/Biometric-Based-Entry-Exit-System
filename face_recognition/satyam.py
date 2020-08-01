from face_recognition import db
from face_recognition.models import Student_details, Leaving_details, History
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,update,column, Integer, String, Table, select, delete
import sqlite3
import cv2
import face_recognition
import numpy as np
import  time
from datetime import datetime
import os

def camera():
	video_capture = cv2.VideoCapture(0)
	connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
	cursor = connection.cursor()
	cursor.execute("""SELECT enrol FROM student_details""")
	position_query = cursor.fetchall()
	known_face_encodings =[]
	known_face_names = []
	for enroll in position_query:
	    string = str(enroll[0] + ".jpeg")
	    image = face_recognition.load_image_file(string)
	    image_encoding=face_recognition.face_encodings(image)[0]
	    known_face_encodings.append(image_encoding)
	    known_face_names.append(enroll)
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True
	name="Unknown"

	while True:
	    ret, frame = video_capture.read()
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	    rgb_small_frame = small_frame[:, :, ::-1]
	    if process_this_frame:
	        # Find all the faces and face encodings in the current frame of video
	        face_locations = face_recognition.face_locations(rgb_small_frame)
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	        face_names = []
	        for face_encoding in face_encodings:
	            # See if the face is a match for the known face(s)
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	            name = "Unknown"
	            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
	            best_match_index = np.argmin(face_distances)
	            if matches[best_match_index]:
	                name = known_face_names[best_match_index]

	            face_names.append(name)

	        process_this_frame = not process_this_frame
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4
					    # Draw a box around the face
		    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		    # Draw a label with a name below the face
		    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		    font = cv2.FONT_HERSHEY_DUPLEX
		# cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

		# Display the resulting image
		cv2.imshow('Video', frame)
		show()
		time.sleep(0.01)

		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
	    if len(face_encodings)!=0:
	    	break
	video_capture.release()
	cv2.destroyAllWindows()
	if name=="Unknown":
	    return name
	return name[0]