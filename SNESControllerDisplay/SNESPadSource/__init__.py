'''
Created on March 15, 2014

@author: Domali
'''
import pygame, sys, serial, datetime, time
import SNESController
from pygame.locals import *
from serial import tools
from serial.tools.list_ports import grep
from datetime import datetime
from datetime import timedelta

#Initialize the GUI and set the resolution
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 265))

def main():
    pygame.display.set_caption('Domalix SNES Controller Display')

    #The following code assumes that there is only one device in a COM port
    #referring to itself as Teensy. If that isn't the case then the following
    #line will have to be modified in order to open the correct COM port to
    #read from.
    try:
        ser = serial.Serial(list(
                serial.tools.list_ports.grep(   # @UndefinedVariable
                    "Teensy"))[0][0],57600)
    except:
        print "Device not found."
        sys.exit()

    controller = SNESController.SNESController(DISPLAYSURF)
    time_list = []
    time_delay = 0
    
    while True: # main game loop
        data = ser.readline().rstrip()
        current_time = datetime.now()
        time_list.append([current_time,data])
        difference = current_time - time_list[0][0]
        difference = (difference.days * 24 * 60 * 60 + difference.seconds) * 1000 + difference.microseconds / 1000
        if difference > time_delay:
            controller.buttonUpdate(time_list.pop(0)[1])
        
        for event in pygame.event.get():
            if event.type == QUIT:
                ser.close()
                controller.quit()
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()