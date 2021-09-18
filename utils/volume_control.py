from pygame.constants import BLEND_ALPHA_SDL2
from utils.setings import VOLUME_BAR_X, VOLUME_BAR_Y, VOLUME_BAR_WIDTH, VOLUME_BAR_HEIGHT, BLACK, DARK_GREEN, GREEN, WHITE, WIDTH
import pygame

class Volume_bar:
    def __init__(self):
        self.x = VOLUME_BAR_X
        self.y = VOLUME_BAR_Y
        self.width = VOLUME_BAR_WIDTH
        self.height = VOLUME_BAR_HEIGHT
        self.volume = 1.0
        self.volume_x = self.x + self.width

    def is_relised(self, mouse_pos, mouse_button):
        mouse_x, mouse_y = mouse_pos
        if self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.width: 
            if mouse_button[0]:
                return True
        return False

    def change_volume(self, mouse_pos, event):
        if self.is_relised(mouse_pos, event):
            mouse_x = mouse_pos[0]
            self.volume_x = mouse_x
            temp_x = mouse_x - self.x
            self.volume = temp_x / self.width
            pygame.mixer.music.set_volume(self.volume)

    def draw(self, win):
        line_width = 3
        points = ((self.x, self.y + self.height), (self.x + self.width, self.y + self.height), (self.x + self.width, self.y))
        pygame.draw.polygon(win, WHITE, points)
        
        if self.volume > 0:
            points2 = ((self.x, self.y + self.height), (self.volume_x, self.y + (self.height - self.height * self.volume)),  (self.volume_x, self.y + self.height))
            pygame.draw.polygon(win, GREEN, points2)
            pygame.draw.polygon(win, BLACK, points2, 1)  
        if pygame.mixer.music.get_volume() == 0.0:
            pygame.draw.polygon(win, WHITE, points)    
        pygame.draw.polygon(win, BLACK, points, 1)
