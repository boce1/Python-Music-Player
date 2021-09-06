import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (86, 209, 48)
DARK_GREEN = (0, 36, 5)
GRAY = (50, 50, 50)
LIGHT_GRAY = (180,180, 180)

WIDTH = 1000
HEIGHT = 800

CONTROL_BAR_HEIGHT = 100
CONTROL_BAR_Y = HEIGHT - CONTROL_BAR_HEIGHT

font_size = 20

FPS = 60

def toolbar_button_y_position(size):
    return CONTROL_BAR_Y + CONTROL_BAR_HEIGHT // 2 - size // 2

SCROLL_SPEED = font_size * 2

GAP = 20

play_image = pygame.image.load(".\\images\\play.png")
pause_image = pygame.image.load(".\\images\\pause.png")
mute_button_on_image = pygame.image.load(".\\images\\mute_on.png")
mute_button_off_image = pygame.image.load(".\\images\\mute_off.png")
replay_button_image = pygame.image.load(".\\images\\replay.png")

PLAY_BUTTON_SIZE = play_image.get_width()
#PLAY_BUTTON_SIZE = 80
PLAY_BUTTON_X = WIDTH // 2 - PLAY_BUTTON_SIZE // 2
PLAY_BUTTON_Y = toolbar_button_y_position(PLAY_BUTTON_SIZE)

MUTE_BUTTON_SIZE = mute_button_on_image.get_width()
MUTE_BUTTON_X = GAP
MUTE_BUTTON_Y = toolbar_button_y_position(MUTE_BUTTON_SIZE)

REPLAY_BUTTON_SIZE = replay_button_image.get_width()
#REPLAY_BUTTON_X = MUTE_BUTTON_X + MUTE_BUTTON_SIZE + GAP
REPLAY_BUTTON_X = PLAY_BUTTON_X - PLAY_BUTTON_SIZE - GAP
REPLAY_BUTTON_Y = toolbar_button_y_position(REPLAY_BUTTON_SIZE)

SONGS_X = 5

SLIDE_BAR_HEIGHT = 20
SLIDE_BAR_Y = HEIGHT - CONTROL_BAR_HEIGHT - SLIDE_BAR_HEIGHT


