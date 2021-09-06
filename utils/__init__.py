from .setings import *
from .button import *
from .song_and_controls import *
from utils._path_ import *

import pygame
pygame.init()
pygame.font.init() # da vidim da li ce mi i ovdea treba deka go imam i u song.py

font = pygame.font.SysFont("Consolas", font_size)

from tkinter import Tk
from tkinter.filedialog import askdirectory
#path = askdirectory(title='Select Folder') # shows dialog box and return the path


# WIDTH // 2 - PLAY_BUTTON_SIZE // 2, CONTROL_BAR_Y + CONTROL_BAR_HEIGHT // 2 - PLAY_BUTTON_SIZE // 2

