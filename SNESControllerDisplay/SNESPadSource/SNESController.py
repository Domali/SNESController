'''
Created on Apr 13, 2014

@author: Domali

Description: A class for displaying SNES Controller input on a PyGame surface
'''
import pygame
import controllerButton
import os

class SNESController:
    def loadConfig(self,button_list):
        f = open('button.cfg','r')
        for line in f:
            if line.split(":")[0] == "BaseImage":
                self.base_image_string = line.rstrip().split(":")[1]
            else:
                button_list.append(controllerButton.controllerButton(
                                                line.rstrip().split(",")))
        f.close()

    def saveConfig(self):
        os.rename('button.cfg','button.cfg.tmp')
        f = open('button.cfg','w')
        config_file_data = "BaseImage:" + self.base_image_string + '\n'
        for i in self.button_list:
            config_file_data += i.toString() + '\n'
        config_file_data = config_file_data.rstrip()
        f.write(config_file_data)
        os.remove('button.cfg.tmp')
        f.close()
        
    def quit(self):
        self.saveConfig()

    #Function to update the button data
    def buttonUpdate(self,data):
        self.displaySurface.blit(self.base_image,(0,0))
        xBase = 0
        yBase = 202
        change = False
        for i in self.button_list:
            if data[-(i.getButtonBit() + 3)] == '0':
                i.incrementTime()
                if i.getPreviousState() == False:
                    change = True
                    i.buttonPressed()
                self.displaySurface.blit(
                            i.getImage(),(i.getImageX(),i.getImageY()))
            else:
                i.buttonNotPressed()
        '''
        The following section was hacked together because evidentally
        python doesn't like doing a whole lot of text rendering... so now
        I'm only rendering text when a button change happens.  Before this code
        was located in the previous for loop and simply rendered the text every
        time.  This is code that needs to be looked into
        '''
        if change == True:
            pygame.draw.rect(self.displaySurface,(0,0,0),(xBase,yBase,400,80))
            for i in self.button_list:
                self.printText(i.getButtonText(),
                               xBase + i.getTextX(), 
                               yBase + i.getTextY())
                self.printText(str(i.getSessionMileage()),
                               xBase + i.getTextX() + i.getTextOffset(), 
                               yBase + i.getTextY())
    def printText(self,text,x,y):
        font = pygame.font.Font(None, 24)
        text = font.render(text, 0, (255, 255, 255))
        textpos = (x,y)
        self.displaySurface.blit(text, textpos)
        
    def __init__(self,pysurface):
        #The surface to print to
        self.displaySurface = pysurface
        self.base_image_string = ""
        self.button_list = []
        self.loadConfig(self.button_list)
        self.base_image = pygame.image.load(self.base_image_string)