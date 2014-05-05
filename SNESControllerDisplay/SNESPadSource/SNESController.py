'''
Created on Apr 13, 2014

@author: Domali

Description: A class for displaying SNES Controller input on a PyGame surface
'''
import pygame
import controllerButton
import os
from datetime import datetime
from datetime import timedelta

class SNESController:
    def __init__(self,pysurface):
        #The surface to print to
        self.xBase = 0
        self.yBase = 202
        self.delay = 0
        self.displaySurface = pysurface
        self.base_image_string = None
        self.button_list = []
        self.loadConfig(self.button_list)
        self.base_image = pygame.image.load(self.base_image_string)
        self.displaySurface.blit(self.base_image,(0,0))
        self.mileageDisplayUpdate()
        self.logging_file_name = None
        self.logging_file = None
        self.logging_state = False
        self.time_list = []
        self.logging_start_time = None


    def loadConfig(self,button_list):
        f = open('button.cfg','r')
        for line in f:
            if line.split(":")[0] == "BaseImage":
                self.base_image_string = line.rstrip().split(":")[1]
            elif line.split(":")[0] == "Delay":
                self.delay = int(line.rstrip().split(":")[1])
            else:
                button_list.append(controllerButton.controllerButton(
                                                line.rstrip().split(",")))
        f.close()

    def saveConfig(self):
        os.rename('button.cfg','button.cfg.tmp')
        f = open('button.cfg','w')
        config_file_data = "BaseImage:" + self.base_image_string + '\n'
        config_file_data += "Delay:" + str(self.delay) + '\n'
        for i in self.button_list:
            config_file_data += i.toString() + '\n'
        config_file_data = config_file_data.rstrip()
        f.write(config_file_data)
        f.close()
        os.remove('button.cfg.tmp')

    def quit(self):
        self.saveConfig()
        if self.logging_state == True:
            self.logging_file.close()

    def update(self,data):
        current_time = datetime.now()
        self.time_list.append([current_time,data])
        difference = current_time - self.time_list[0][0]
        difference = (difference.days * 24 * 60 * 60 + \
                      difference.seconds) * 1000 + \
                      difference.microseconds / 1000
        if difference > self.delay:
            self.buttonUpdate(self.time_list.pop(0)[1])
        self.logData(data,current_time)    
        
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

    def startLogging(self):
        self.logging_state = True
        self.logging_start_time = datetime.now()
        self.logging_file_name = '%i_%i_%i_%i_%i_Controller.log' % (
                    self.logging_start_time.year,
                    self.logging_start_time.month,
                    self.logging_start_time.day,
                    self.logging_start_time.minute,
                    self.logging_start_time.second)
        self.logging_file = open(self.logging_file_name,'a') 
        self.logging_file.write('timestamp' + '\t' + 'controllerRecord' + '\n')

    def stopLogging(self):
        self.logging_state = False
        self.logging_file.close()
        
    def toggleLogging(self):
        if self.logging_state == False:
            self.startLogging()
        else:
            self.stopLogging()
    def logData(self,data,current_time):
        if self.logging_state == True:
            difference = current_time - self.logging_start_time
            difference = (difference.days * 24 * 60 * 60 + \
                      difference.seconds) * 1000 + \
                      difference.microseconds / 1000
            self.logging_file.write(str(difference) + '\t' + str(data) + '\n')

    def setDelay(self, delay_ms):
        self.delay = delay_ms