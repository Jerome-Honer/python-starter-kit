import cv2
import sys
import serial
import serial.tools.list_ports
import time
ports = serial.tools.list_ports.comports()

portlst = []

for port, desc, hwid in sorted(ports):
    portlst.append(port)
    print("{}: {} [{}]".format(port, desc, hwid))


arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)

cascPath = r'C:\Users\Jerome\Desktop\python\turret\haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    xcor = 0
    ycor = 0
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(f"the x y coardinates are {x} {y}")
        xcor = x
        ycor = y
    xcor = xcor / 300
    xcor = xcor * 180
    ycor = ycor / 300
    ycor = ycor * 180    
    arduino.write(bytes(str(xcor),"utf-8"))
    time.sleep(0.05)
    arduino.write(bytes(str(ycor),"utf-8"))
    time.sleep(0.05)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()