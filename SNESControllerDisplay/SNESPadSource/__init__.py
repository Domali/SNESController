'''
Created on March 15, 2014

@author: Domali
'''
import pygame, sys, serial, datetime, time
import SNESController
from pygame.locals import *
from serial import tools
from serial.tools.list_ports import grep

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
    while True: # main game loop
        data = ser.readline()
        controller.buttonUpdate(data)

        for event in pygame.event.get():
            if event.type == QUIT:
                ser.close()
                controller.quit()
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()