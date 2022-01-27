import face_recognition
import os
import cv2
import numpy as np

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

known_person=[]
known_image=[] 
known_face_encodings=[] 

face_locations = []
face_encodings = []
face_names = []
frame_processed = True

for file in os.listdir("profiles"):
    try:
        #extract person's name
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("profiles/", file)
        known_image = face_recognition.load_image_file(file)
        #print(face_recognition.face_encodings(known_image)[0])
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
        #print(known_face_encodings)

    except Exception as e:
        pass
    
#print(len(known_face_encodings))
#print(known_person)



class VideoCamera(object):
    global current_person;
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_person(self):
        return self.current_person
    
    def get_frame(self):
        success, image = self.video.read()
        
        frame_processed = True
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

        #BGR to RGB color conversion (to allow face_recognition to be able to read it)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        #processing once every 2 frames
        if frame_processed:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            global name_onScreen;

            for face_encoding in face_encodings:
                #check for matching face
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unrecognized"
                
                #print(face_encoding)
                print(matches)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_person[best_match_index]

                print(name)
                #print(face_locations)
                face_names.append(name)
        
                name_onScreen = name
                current_person = name

        frame_processed = not frame_processed
            
        #display
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            #drawing a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            #labeling the box
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name_onScreen, (left + 10, bottom - 10), font, 1.0, (0, 0, 0), 1)

        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
