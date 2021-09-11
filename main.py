from utils import *

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

root = Tk()
root.withdraw()

play_button = Play_button(PLAY_BUTTON_X, PLAY_BUTTON_Y, PLAY_BUTTON_SIZE)
replay_button = Replay_button(REPLAY_BUTTON_X, REPLAY_BUTTON_Y, REPLAY_BUTTON_SIZE)
mute_button = Mute_button(MUTE_BUTTON_X, MUTE_BUTTON_Y, MUTE_BUTTON_SIZE)
loop_button = Loop_button(LOOP_BUTTON_X, LOOP_BUTTON_Y, LOOP_BUTTON_SIZE)
forward_button = Forward_button(FORWARD_BUTTON_X, FORWARD_BUTTON_Y, FORWARD_BUTTON_SIZE)
backward_button = Backward_button(BACKWARD_BUTTON_X, BACKWARD_BUTTON_Y, BACKWARD_BUTTON_SIZE)

toolbar_buttons = (play_button, replay_button, mute_button, loop_button, backward_button, forward_button)

def if_songs_empty(song_list):
    empty_list_message = font.render(f"Location {path} is empty.", True, GREEN)
    window.blit(empty_list_message, (WIDTH // 2 - empty_list_message.get_width() // 2, 20))    

def draw_control_bar(win, y, height):
    pygame.draw.rect(win, GRAY, (0, y, WIDTH, height))
    pygame.draw.rect(win, GREEN, (0, y, WIDTH, height), 1)

def draw_slide_bar(win, y, height):
    pygame.draw.rect(win, GRAY, (0, y, WIDTH, height))
    pygame.draw.rect(win, GREEN, (0, y, WIDTH, height), 1)


def main_draw(win, mouse_position, mouse_pressed, buttons = toolbar_buttons):
    win.fill(BLACK)
    if songs_on_screen > 0:
        for song in songs:
            song.draw(win, mouse_position, mouse_pressed)
    else:
        if_songs_empty(songs)
    draw_control_bar(window, CONTROL_BAR_Y, CONTROL_BAR_HEIGHT)
    draw_slide_bar(window, SLIDE_BAR_Y, SLIDE_BAR_HEIGHT)
    draw_playing_song(window)
    for button in buttons:
        button.draw(win, mouse_position, mouse_pressed)
        button.draw_sign(window)
    #loop_button.draw(win, mouse_position, mouse_pressed)
    

    pygame.display.update()

def scroll(event, bar_y, speed):
    if event.type == pygame.MOUSEWHEEL:
        return event.y * speed
    return 0

def scroll_songs(songs):
    if len(list_of_files) > songs_on_screen:
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
        loop_button.loop(mouse_position, event, list_of_files)
        backward_button.backward(mouse_position, event,list_of_files)
        forward_button.forward(mouse_position, event, list_of_files)


        for song in songs:
            song.play(mouse_position, event, songs)
        #print(pygame.mixer.music.get_busy())
        scroll_songs(songs)
        #print(f"{SONG_END}  :  {loop}")
pygame.quit()
