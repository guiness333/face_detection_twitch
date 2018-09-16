import cv2
import numpy as np
import time
from livestreamer import Livestreamer

session = Livestreamer()
session.set_option("http-headers", "Client-ID=jzkbprff40iqj646a697cyrvl0zt2m6")
streams = session.streams("https://www.twitch.tv/___")
stream = streams['best']


classificador = cv2.CascadeClassifier("./haarcascade-frontalface-default.xml")

fname = "test.mpg"
vid_file = open(fname,"wb")
fd = stream.open()
for i in range(0,2*2048):
    if i%256==0:
        print("Buffering...")
    new_bytes = fd.read(1024)
    vid_file.write(new_bytes)
print("Done buffering.")
cam = cv2.VideoCapture(fname)
while True:
    ret, img = cam.read()                      
    try:
        if ret:
            imagemCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            facesDetectadas = classificador.detectMultiScale(imagemCinza,
                                                    scaleFactor=1.5,
                                                    minSize=(100,100))
            print(facesDetectadas)
            for (x, y, l, a) in facesDetectadas:
                cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
            #img = 255-img # invert the colors
            cv2.imshow('live_img',img)
    except:
        print("URGH")
        continue
    if (0xFF & cv2.waitKey(5) == 27) or img.size == 0:
        break
    time.sleep(0.05) 
    new_bytes = fd.read(1024*16)
    vid_file.write(new_bytes)
vid_file.close()
fd.close()