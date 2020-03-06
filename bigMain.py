#Copyright (c) 2020 Derek Frombach

#Python Video Streaming Client with MJPEG decoder
#Compatible with almost every TCP MJPEG server
#Runs in near Real-Time
#Client Runs on Linux/Windows
import cv2
import socket
import numpy as np

buff=1500 #Don't change this
host='localhost' #Change this to your server address
port=8080 #Change this to your server port

#Opening the remote IP and initalizing recieve buffer
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
s.connect((host,port))
c = b''

#Function call speedups
show=cv2.imshow
dec=cv2.imdecode
waitK=cv2.waitKey
nfs=np.frombuffer
uint8=np.uint8
colour=cv2.IMREAD_COLOR
flip=cv2.flip
ur=s.recv
rdwr=socket.SHUT_RDWR

#Capture loop
s.send(b'\x00\x00')
while True:
    c += ur(buff) #Recieve information and add to buffer
    #Check for JPEG beginning and end
    a = c.find(b'\xff\xd8') 
    b = c.find(b'\xff\xd9')
    if a != -1 and b != -1: #Found JPEG beginning and end
        #Decoding
        jpg = c[a:b+2]
        c = c[b+2:] #Clear Buffer
        i = dec(nfs(jpg, dtype=uint8), colour)
        #Displaying
        show('i',i)
        if waitK(1) == ord('q'): #EXIT KEY IS 'q'
            s.shutdown(rdwr)
            s.close()
            cv2.destroyAllWindows()
            break
