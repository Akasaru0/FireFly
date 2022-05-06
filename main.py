from base64 import decode
from socket import *
from threading import *
import time, pygame
from pygame.locals import *

takeoff = False



def fonction():
    m = ""
    for event in pygame.event.get():
        
        if event.type == JOYBUTTONDOWN:
            # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
            if event.button == 0 and takeoff == False:
                print("A")
                m= "takeoff"
            if event.button == 1:
                print("B")
                m= "emergency"
            if event.button == 2:
                print("X")
            if event.button == 3:
                print("Y")
                m= "land"
            if event.button == 4:
                print("LB")
            if event.button == 5:
                print("RB")
            
        #if event.type == JOYBUTTONUP:
        #    print("Button up")
        if event.type == JOYAXISMOTION:
            a = 0
            b = 0
            c = 0
            d = 0
            if event.axis == 0:

                print("joy Gauche - X Value : "+str(round(event.value,2)))
                b = event.value*100
                    
            if event.axis == 1:
                print("joy Gauche - Y Value : "+str(round(event.value,2)))
                a = event.value*100
            if event.axis == 2:
                print("joy Droit - X Value : "+str(round(event.value,2)))
            if event.axis == 3:
                print("joy Droit - Y Value : "+str(round(event.value,2)))
            if event.axis == 4:
                print("Gachette Gauche Value : "+str(round((1+event.value)/2,2)))
            if event.axis == 5:
                print("Gachette Droite Value : "+str(round((1+event.value)/2,2)))
            m = "rc "+str(a)+" "+str(b)+" "+str(c)+" "+str(d)+""
    return m


pygame.init()

HOST_IP = "0.0.0.0"
HOST_PORT =  9000
addr_host = (HOST_IP,HOST_PORT)

print("[x] Starting the script")
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print("[x] Joysticks Setup Done\n")

s = socket(AF_INET,SOCK_DGRAM)
s.bind(addr_host)
print("[x] Server Start to listens : "+HOST_IP+":"+str(HOST_PORT)+"\n")


while True:
    print("[x] Trying to connect to the drone")
    s.sendto(("command").encode('utf-8'),("192.168.10.1", 8889))
    if s.recv(1024).decode() == 'ok':
        break
    else:
        time.sleep(2)
#s.sendto(("battery?").encode('utf-8'),("192.168.10.1", 8889))
#print(s.recv(1024).decode())
print('[x] Connection etablished\n')
while True:
    m = fonction()
    if m != "": 
        s.sendto(m.encode(),("192.168.10.1", 8889))
