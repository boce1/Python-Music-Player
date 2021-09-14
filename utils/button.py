from utils.setings import *
import pygame
pygame.mixer.init()

class Button:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def is_pressed(self, mouse_pos, mouse_but):
        mouse_x, mouse_y = mouse_pos
        if self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.width: 
            if mouse_but[0]:
                return True
        return False
        
    def draw(self, win, mouse_pos, mouse_but):
        if not self.is_pressed(mouse_pos, mouse_but):
            pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.width))
        else:
            pygame.draw.rect(win, LIGHT_GRAY, (self.x, self.y, self.width, self.width))
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.width), 1)

    def is_ready(self, mouse_pos, event):
        mouse_x, mouse_y = mouse_pos
        if self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.width: 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False

    def is_relised(self, mouse_pos, event):
        mouse_x, mouse_y = mouse_pos
        if self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.width: 
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                return True
        return False