import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (86, 209, 48)
DARK_GREEN = (0, 36, 5)
GRAY = (50, 50, 50)
LIGHT_GRAY = (180,180, 180)

WIDTH = 1200
HEIGHT = 740

CONTROL_BAR_HEIGHT = 100
CONTROL_BAR_Y = HEIGHT - CONTROL_BAR_HEIGHT

font_size = 20

SONG_BOX_SIZE = font_size

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
loop_button_on_image = pygame.image.load(".\\images\\loop_on.png")
loop_button_off_image = pygame.image.load(".\\images\\loop_off.png")
forwad_button_image = pygame.image.load(".\\images\\forward.png")
backward_button_image = pygame.image.load(".\\images\\backward.png")
save_button_image = pygame.image.load(".\\images\\save.png")
loop_one_button_image = pygame.image.load(".\\images\\loop_one.png")

PLAY_BUTTON_SIZE = play_image.get_width()
#PLAY_BUTTON_SIZE = 80
PLAY_BUTTON_X = WIDTH // 2 - PLAY_BUTTON_SIZE // 2
PLAY_BUTTON_Y = toolbar_button_y_position(PLAY_BUTTON_SIZE)

MUTE_BUTTON_SIZE = mute_button_on_image.get_width()
MUTE_BUTTON_X = GAP
MUTE_BUTTON_Y = toolbar_button_y_position(MUTE_BUTTON_SIZE)

SAVE_BUTTON_SIZE = save_button_image.get_width()
SAVE_BUTTON_X = MUTE_BUTTON_X + MUTE_BUTTON_SIZE + GAP
SAVE_BUTTON_Y = toolbar_button_y_position(SAVE_BUTTON_SIZE)

REPLAY_BUTTON_SIZE = replay_button_image.get_width()
#REPLAY_BUTTON_X = MUTE_BUTTON_X + MUTE_BUTTON_SIZE + GAP
REPLAY_BUTTON_X = PLAY_BUTTON_X  - GAP - REPLAY_BUTTON_SIZE
REPLAY_BUTTON_Y = toolbar_button_y_position(REPLAY_BUTTON_SIZE)

LOOP_BUTTON_SIZE = loop_button_on_image.get_width()
LOOP_BUTTON_X = REPLAY_BUTTON_X - GAP - LOOP_BUTTON_SIZE
LOOP_BUTTON_Y = toolbar_button_y_position(LOOP_BUTTON_SIZE)

BACKWARD_BUTTON_SIZE = backward_button_image.get_width()
BACKWARD_BUTTON_X = PLAY_BUTTON_X + PLAY_BUTTON_SIZE + GAP
BACKWARD_BUTTON_Y = toolbar_button_y_position(BACKWARD_BUTTON_SIZE)

FORWARD_BUTTON_SIZE = forwad_button_image.get_width()
FORWARD_BUTTON_X = BACKWARD_BUTTON_X + BACKWARD_BUTTON_SIZE + GAP
FORWARD_BUTTON_Y = toolbar_button_y_position(FORWARD_BUTTON_SIZE)

SONGS_X = 5

SLIDE_BAR_HEIGHT = 20
SLIDE_BAR_Y = HEIGHT - CONTROL_BAR_HEIGHT - SLIDE_BAR_HEIGHT - SONG_BOX_SIZE

SONG_PLALYING_TEXT = SLIDE_BAR_Y + SONG_BOX_SIZE
SONG_PLALYING_TEXT_HEIGHT = SONG_BOX_SIZE

VOLUME_BAR_WIDTH = 100
VOLUME_BAR_X = WIDTH - GAP - VOLUME_BAR_WIDTH
VOLUME_BAR_HEIGHT = 50
VOLUME_BAR_Y = toolbar_button_y_position(VOLUME_BAR_HEIGHT) 
