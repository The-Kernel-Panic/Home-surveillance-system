import face_recognition
import cv2
import numpy as np
from twilio.rest import Client

#Twilio
account_sid = "AC83a0f02ff97d49fc8c548186368aab7f"
auth_token = "93b558464309701dc933315a003586ec"
client = Client(account_sid, auth_token)


def afterRec(name):
    if name != "Unknown":
        client.api.account.messages.create(
        to="+919769010076", #Take user input for this
        from_="+13345084553",
        body="Found: {}".format(name))
    elif name == "Unknown":
           client.api.account.messages.create(
           to="+919769010076", #Take user input for this
           from_="+13345084553",
           body="Unknown intruder, Watch the livestream: www.http://192.168.1.105/8000")
           
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("/Users/pb/Desktop/My Folder/Raspberry Pi/Face Recognition/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
michael_image = face_recognition.load_image_file("/Users/pb/Desktop/My Folder/Raspberry Pi/Face Recognition/Michael_Reeves.jpg")
michael_face_encoding = face_recognition.face_encodings(michael_image)[0]

# Load a third sample picture and learn how to recognize it.
piyusha_image = face_recognition.load_image_file("/Users/pb/Desktop/My Folder/Raspberry Pi/Face Recognition/Piyusha_Bhor.jpg")
piyusha_face_encoding = face_recognition.face_encodings(piyusha_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    michael_face_encoding,
    piyusha_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Michael Reeves",
    "Piyusha Bhor"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
count = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
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

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        while count < 1:
            afterRec(name) #This function does whatever we want to do once the face is found.
            count = count + 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
