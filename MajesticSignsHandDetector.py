import cv2
from cvzone.HandTrackingModule import HandDetector
import socket #Needed to send data

#Parameters
width = 1280
height = 720

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#Hand detector
detector = HandDetector(maxHands=2, detectionCon = 0.8)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#SOCK_DGRAM for UDP, SOCK_STREAM for tcp

serverAddressPort = ("127.0.0.1", 10040) 
# Port can be any number. 
# Make sure I don't use the same one when I build the final product after testing
# Just in case

#There are 21 points on each hand

while True:

    succ, img = cap.read()
    hands, img = detector.findHands(img)

    #In case I need to determine which one's the left hand and which one's the right
    #https://github.com/cvzone/cvzone#hand-tracking-module 

    data = []

    if hands:

        for x in range(len(hands)): #Do this for each hand
            hand = hands[x] #Get the hands that are detected
            lmList = hand['lmList'] # Get the landmark list

            #lmList is a dictionary containing the coordinates of each point on a hand

            #To send the information to Unity

            #In cv, the 0,0 origin is top left, the maximum is bottom left
            #In Unity, it's the opposite, which is why height - lm[1] is there
            for lm in lmList:
                data.extend([lm[0], height - lm[1], lm[2]])
            
            sock.sendto(str.encode(str(data)), serverAddressPort)
    else:
        data.extend("") #Since a bytes-like object is required
        sock.sendto(str.encode(str(data)), serverAddressPort)

    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)