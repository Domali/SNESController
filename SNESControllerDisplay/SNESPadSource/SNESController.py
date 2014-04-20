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
        f.close()
        os.remove('button.cfg.tmp')

    def quit(self):
        self.saveConfig()

    #Function to update the button data
    def buttonUpdate(self,data):
        self.displaySurface.blit(self.base_image,(0,0))
        change = False
        for i in self.button_list:
            if data[-(i.getButtonBit() + 1)] == '0':
                i.incrementTime()
                if i.getPreviousState() == False:
                    change = True
                    i.buttonPressed()
                self.displaySurface.blit(
                            i.getImage(),(i.getImageX(),i.getImageY()))
            else:
                i.buttonNotPressed()
        if change == True:
            self.mileageDisplayUpdate()

    def mileageDisplayUpdate(self):
        pygame.draw.rect(self.displaySurface,(0,0,0),
                             (self.xBase,self.yBase,400,80))
        for i in self.button_list:
            self.displaySurface.blit(i.getRenderedText(),
                           (self.xBase + i.getTextX(),
                           self.yBase + i.getTextY()))
            self.displaySurface.blit(i.getMileageImage(),
                           (self.xBase + i.getTextX() + i.getTextOffset(),
                           self.yBase + i.getTextY()))

    def __init__(self,pysurface):
        #The surface to print to
        self.xBase = 0
        self.yBase = 202
        self.displaySurface = pysurface
        self.base_image_string = None
        self.button_list = []
        self.loadConfig(self.button_list)
        self.base_image = pygame.image.load(self.base_image_string)
        self.displaySurface.blit(self.base_image,(0,0))
        self.mileageDisplayUpdate()