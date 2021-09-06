from utils import *

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

root = Tk()
root.withdraw()

play_button = Play_button(PLAY_BUTTON_X, PLAY_BUTTON_Y, PLAY_BUTTON_SIZE)
replay_button = Replay_button(REPLAY_BUTTON_X, REPLAY_BUTTON_Y, REPLAY_BUTTON_SIZE)
mute_button = Mute_button(MUTE_BUTTON_X, MUTE_BUTTON_Y, MUTE_BUTTON_SIZE)


toolbar_buttons = (play_button, replay_button, mute_button)

def draw_control_bar(win, y, height):
    pygame.draw.rect(win, GRAY, (0, y, WIDTH, height))
    pygame.draw.rect(win, GREEN, (0, y, WIDTH, height), 1)

def draw_slide_bar(win, y, height):
    pygame.draw.rect(win, GRAY, (0, y, WIDTH, height))
    pygame.draw.rect(win, GREEN, (0, y, WIDTH, height), 1)

def main_draw(win, mouse_position, mouse_pressed, buttons = toolbar_buttons):
    win.fill(BLACK)
    for song in songs:
        song.draw(win, mouse_position, mouse_pressed)
    draw_control_bar(window, CONTROL_BAR_Y, CONTROL_BAR_HEIGHT)
    draw_slide_bar(window, SLIDE_BAR_Y, SLIDE_BAR_HEIGHT)
    for button in buttons:
        button.draw(win, mouse_position, mouse_pressed)
    play_button.draw_sign(window)
    mute_button.draw_sign(window)

    pygame.display.update()

def scroll(event, bar_y, speed):
    if event.type == pygame.MOUSEWHEEL:
        return event.y * speed
    return 0

def scroll_songs(songs):
    for song in songs:
        if song.y <= song.prev_y:
            song.y += scroll(event, SLIDE_BAR_Y, SCROLL_SPEED)

        if song.y > song.prev_y:
            song.y = song.prev_y

        if song.y < song.next_y:
            song.y = song.next_y

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    mouse_position = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    main_draw(window, mouse_position, mouse_buttons)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        play_button.play(mouse_position, event)
        replay_button.replay(mouse_position, event)
        mute_button.mute(mouse_position, event)

        for song in songs:
            song.play(mouse_position, event, songs)

        scroll_songs(songs)
pygame.quit()
