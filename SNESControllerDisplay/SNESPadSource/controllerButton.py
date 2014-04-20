'''
Created on Apr 19, 2014

@author: Domali
'''
import pygame

class controllerButton(object):
    '''
    classdocs
    '''


    def __init__(self, configuration_list):
        '''
        Constructor
        '''
        self.button_name = configuration_list[0]
        self.x_text_offset = configuration_list[1]
        self.y_text_offset = configuration_list[2]
        self.data_text_offset = configuration_list[3]
        self.image_file = pygame.image.load(configuration_list[4])
        self.image_string = configuration_list[4]
        self.image_x = configuration_list[5]
        self.image_y = configuration_list[6]
        self.bit_offset = configuration_list[7]
        self.total_mileage = int(configuration_list[8])
        self.session_mileage = 0
        self.previous_state = False
        self.unfixed_total_time = 0
        self.font = pygame.font.Font(None, 24)
        self.rendered_text = self.font.render(self.button_name, 0, (255, 255, 255))
        self.renderMileageText()
    
    def getMileageImage(self):
        return self.rendered_mileage_text
        
    def getImage(self):
        return self.image_file
    
    def getButtonBit(self):
        return int(self.bit_offset)
    
    def getPreviousState(self):
        return self.previous_state
    
    def getImageX(self):
        return int(self.image_x)
    
    def getImageY(self):
        return int(self.image_y)
    
    def incrementTime(self):
        self.unfixed_total_time += 1
    
    def renderMileageText(self):
        self.rendered_mileage_text = self.font.render(
                                str(self.session_mileage), 0, (255, 255, 255))
        
    def buttonPressed(self):
        self.previous_state = True
        self.session_mileage += 1
        self.total_mileage += 1
        self.renderMileageText()
        
    def buttonNotPressed(self):
        self.previous_state = False
        
    def getButtonText(self):
        return self.button_name
    
    def getTextX(self):
        return int(self.x_text_offset)
    
    def getTextY(self):
        return int(self.y_text_offset)
    
    def getTextOffset(self):
        return int(self.data_text_offset)
    
    def getSessionMileage(self):
        return int(self.session_mileage)
    
    def getRenderedText(self):
        return self.rendered_text
    
    def toString(self):
        return self.__str__()

    def __str__(self):
        return self.button_name + "," + self.x_text_offset + "," \
            + self.y_text_offset + "," + self.data_text_offset + "," \
            + self.image_string + ","  + self.image_x + "," \
            + self.image_y + "," + self.bit_offset + "," \
            + str(self.total_mileage)