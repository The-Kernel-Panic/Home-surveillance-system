# AI Home Surveillance-System
A surveillance system.

#How it works

The Raspberry Pi runs a face recognition code. If a face is detected, the code determines if the person is known or unknown. 
In case the person is known, the pi sends a message to the user with the name of the person found.
In case the person is unknown, the pi sends a message to the user with the image of the person found.
The apache server running on the pi is used to store these images and we can send the link of this image to the user via the Twilio API.


#Requirements:

Hardware:
1. Raspberry Pi (any version)
2. A Raspberry Pi camera module

Python modules: 
1. os
2. face_recognition
3. cv2
4. numpy
5. twilio

Make sure to change the code according to your Pi's ip and directory path.

To use the Twilio API make an free account on https://www.twilio.com/try-twilio.

Also you should run an apache server on the pi. You can read this if you are stuck: https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md

Note: In case you have trouble installing face recognition module make sure you have installed all the necessary libraries for it. You can refer to this: https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65
