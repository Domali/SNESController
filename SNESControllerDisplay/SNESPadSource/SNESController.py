'''
Created on Apr 13, 2014

@author: Domali

Description: A class for displaying SNES Controller input on a PyGame surface
'''
import pygame
class SNESController:
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
    
    #Function to update the button data
    def update(self,data):
        self.displaySurface.blit(self.SNESBaseImg,(0,0))
        self.buttonUpdate(self.BImg,self.BTN_B,data)
        self.buttonUpdate(self.AImg,self.BTN_A,data)
        self.buttonUpdate(self.XImg,self.BTN_X,data)
        self.buttonUpdate(self.YImg,self.BTN_Y,data)
        self.buttonUpdate(self.StartImg,self.BTN_START,data)
        self.buttonUpdate(self.SelectImg,self.BTN_SELECT,data)
        self.buttonUpdate(self.LImg,self.BTN_L,data)
        self.buttonUpdate(self.RImg,self.BTN_R,data)
        self.buttonUpdate(self.DPadLeftImg,self.BTN_DPL,data)
        self.buttonUpdate(self.DPadRightImg,self.BTN_DPR,data)
        self.buttonUpdate(self.DPadUpImg,self.BTN_DPU,data)
        self.buttonUpdate(self.DPadDownImg,self.BTN_DPD,data)
        
    def buttonUpdate(self,img,btn,data):
        if data[-(btn + 3)] == '0':
            if self.btnPrev[btn] == 0:
                self.btnArray[btn] += 1
                self.btnPrev[btn] = 1
                self.updateButtonUsageDisplay()
            self.displaySurface.blit(img,(int(self.xyConfig[btn][0]),
                                          int(self.xyConfig[btn][1])))
        else:
            self.btnPrev[btn] = 0

    def printText(self,text,x,y):
        font = pygame.font.Font(None, 24)
        text = font.render(text, 0, (255, 255, 255))
        textpos = (x,y)
        self.displaySurface.blit(text, textpos)
        
    def updateButtonUsageDisplay(self):
        xBase = 0
        yBase = 202
        pygame.draw.rect(self.displaySurface,(0,0,0),(0,201,400,80))
        self.printText("A:",xBase,yBase)
        self.printText(str(self.btnArray[self.BTN_A]),xBase + 20,yBase)
        self.printText("B:",xBase + 1, yBase + 15)
        self.printText(str(self.btnArray[self.BTN_B]),xBase + 20, yBase + 15)
        self.printText("X:",xBase + 1, yBase + 30)
        self.printText(str(self.btnArray[self.BTN_X]), xBase + 20, yBase + 30)
        self.printText("Y:", xBase + 2, yBase + 45)
        self.printText(str(self.btnArray[self.BTN_Y]),xBase + 20, yBase + 45)
        self.printText("Up:", xBase + 133, yBase)
        self.printText(str(self.btnArray[self.BTN_DPU]),xBase + 183, yBase)
        self.printText("Down:", xBase + 133, yBase + 15)
        self.printText(str(self.btnArray[self.BTN_DPD]), xBase + 183, yBase + 15)
        self.printText("Left:", xBase + 133, yBase + 30)
        self.printText(str(self.btnArray[self.BTN_DPL]), xBase + 183, yBase + 30)
        self.printText("Right:", xBase + 133, yBase + 45)
        self.printText(str(self.btnArray[self.BTN_DPR]), xBase + 183, yBase + 45)
        self.printText("L:", xBase + 266, yBase)
        self.printText(str(self.btnArray[self.BTN_L]), xBase + 330, yBase)
        self.printText("R:", xBase + 266, yBase + 15)
        self.printText(str(self.btnArray[self.BTN_R]), xBase + 330, yBase + 15)
        self.printText("Select:", xBase + 266, yBase + 30)
        self.printText(str(self.btnArray[self.BTN_SELECT]), xBase + 330, yBase + 30)
        self.printText("Start:", xBase + 266, yBase + 45)
        self.printText(str(self.btnArray[self.BTN_START]), xBase + 330, yBase + 45)
        
    def __init__(self,pysurface):
        #The surface to print to
        self.displaySurface = pysurface

        #A couple variables to keep track of buttons being pressed
        self.btnArray = range(12)
        self.btnPrev = range(12)
        for i in self.btnArray:
            self.btnArray[i] = 0
            self.btnPrev[i] = 0
        self.updateButtonUsageDisplay()
        #Variable to hold the x and y configuration fort he images
        self.xyConfig = []
        config = open('images.cfg','r')
        for line in config:
            self.xyConfig.append(line[:-1].split()[1].split(","))
        config.close()