import pygame
import serial
import time

port = '/dev/ttyUSB1'

rteq = serial.Serial(port,115200,timeout = 0.1);

speed = 300

#user input
while True:
    pygame.display.set_mode((640,480))
    pygame.event.get()
    keyP = pygame.key.get_pressed()
    if keyP[pygame.K_UP]:
        rteq.write("!G 1 "+ str(speed) +"\r!G 2 " + str(speed) + "\r")
        print "up"
    elif keyP[pygame.K_DOWN]:
        rteq.write("!G 1 -"+ str(speed) +"\r!G 2 -" + str(speed) + "\r")
        print "down"
    elif keyP[pygame.K_LEFT]:
        rteq.write("!G 1 0\r!G 2 " + str(speed) +"\r")
        print "left"
    elif keyP[pygame.K_RIGHT]:
        rteq.write("!G 1 " + str(speed) + "\r!G 2 0\r")
        print "right"
    elif keyP[pygame.K_ESCAPE]:
        pygame.display.quit
        print "escape"
        break
    else:
        rteq.write("!G 1 0\r!G 2 0\r")
        print "stop"

rteq.close()
pygame.quit()
