'''
Created on March 15, 2014

@author: Domali
'''
import pygame, sys, serial, datetime, time
from pygame.locals import *
from serial import tools
from serial.tools.list_ports import grep

#Initialize the GUI and set the resolution
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 200))

# Load all of the images that we need to create the controller
SNESBaseImg = pygame.image.load("..\ArtAssets\SNESBase.png")
AImg = pygame.image.load("..\ArtAssets\A.png")
BImg = pygame.image.load("..\ArtAssets\B.png")
XImg = pygame.image.load("..\ArtAssets\X.png")
YImg = pygame.image.load("..\ArtAssets\Y.png")
DPadLeftImg = pygame.image.load("..\ArtAssets\DPadLeft.png")
DPadRightImg = pygame.image.load("..\ArtAssets\DPadRight.png")
DPadUpImg = pygame.image.load("..\ArtAssets\DPadUp.png")
DPadDownImg = pygame.image.load("..\ArtAssets\DPadDown.png")
SelectImg = pygame.image.load("..\ArtAssets\Select.png")
StartImg = pygame.image.load("..\ArtAssets\Start.png")
LImg = pygame.image.load("..\ArtAssets\L.png")
RImg = pygame.image.load("..\ArtAssets\R.png")

#How many bits from the final bit in the data that our button bit is at.
#Refer to how the SNES Controller communicates to understand which bit
#each button is at.
BTN_B = 0
BTN_Y = 1
BTN_SELECT = 2
BTN_START = 3
BTN_DPU = 4
BTN_DPD = 5
BTN_DPL = 6
BTN_DPR = 7
BTN_A = 8
BTN_X = 9
BTN_L = 10
BTN_R = 11

#A couple variables to keep track of how many times a button has been pressed
#as well as if the button has been let go since its last press.
btnArray = range(12)
btnPrev = range(12)
for i in btnArray:
    btnArray[i] = 0
    btnPrev[i] = 0

timeQueue = []
buttonsQueue = []

#The following code opens the image config file and then strips the new line
#and button name out of it.  It then loads these tuples into the array
#that holds the configuration for X and Y coordinates.
xyConfig = []
config = open('images.cfg','r')
for line in config:
    xyConfig.append(line[:-1].split()[1].split(","))
config.close()

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

    while True: # main game loop
        if ser.inWaiting() > 0:
            DISPLAYSURF.blit(SNESBaseImg,(0,0))
            data = ser.readline()
            buttonUpdate(BImg,BTN_B,data)
            buttonUpdate(AImg,BTN_A,data)
            buttonUpdate(XImg,BTN_X,data)
            buttonUpdate(YImg,BTN_Y,data)
            buttonUpdate(StartImg,BTN_START,data)
            buttonUpdate(SelectImg,BTN_SELECT,data)
            buttonUpdate(LImg,BTN_L,data)
            buttonUpdate(RImg,BTN_R,data)
            buttonUpdate(DPadLeftImg,BTN_DPL,data)
            buttonUpdate(DPadRightImg,BTN_DPR,data)
            buttonUpdate(DPadUpImg,BTN_DPU,data)
            buttonUpdate(DPadDownImg,BTN_DPD,data)

        for event in pygame.event.get():
            if event.type == QUIT:
                ser.close()
                pygame.quit()
                sys.exit()
        pygame.display.update()

def buttonUpdate(img,btn,data):
    if data[-(btn + 3)] == '0':
        if btnPrev[btn] == 0:
            btnArray[btn] += 1
            btnPrev[btn] = 1
        DISPLAYSURF.blit(img,(int(xyConfig[btn][0]),int(xyConfig[btn][1])))
    else:
        btnPrev[btn] = 0

if __name__ == "__main__":
    main()
