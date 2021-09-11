from utils.setings import *
from utils._path_ import list_of_files, path
from utils.button import *
import pygame
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Consolas", font_size)

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
loop = False
pause = False
is_muted = False
song_index = 0
class Song:
    songs_num = 0
    def __init__(self, name, y, index):
        self.name = name
        self.y = y
        self.prev_y = self.y
        self.next_y = 0
        self.index = index
        self.message = font.render(self.name.replace(".mp3", ""), True, GREEN)
        self.width = self.message.get_width()
        self.height = self.message.get_height() 
        self.x = 0
        self.left = True

    def is_mouse_pointing(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if 0 < mouse_x < WIDTH and \
            self.y < mouse_y < self.y + self.height:
            if not (self.y >= SLIDE_BAR_Y):
                return True
        return False 

    def is_clicked(self, mouse_pos, mouse_but):
        if self.is_mouse_pointing(mouse_pos):
            if mouse_but[0]:
                return True
        return False

    def is_chosen(self, mouse_pos, event):
        if self.is_mouse_pointing(mouse_pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False

    def draw(self, win, mouse_pos, mouse_but):
        if self.is_mouse_pointing(mouse_pos):
            if SONGS_X + self.width > WIDTH:
                if self.left:
                    self.x -= 1
                if self.x <= WIDTH - self.width:
                    self.left = False
                if not self.left:
                    self.x += 1
                if self.x >= 0:
                    self.left = True
        else:
            self.x = 0

        if self.is_clicked(mouse_pos, mouse_but):
            if self.width < WIDTH:
                pygame.draw.rect(win, LIGHT_GRAY, (self.x, self.y, WIDTH, self.height))
            else:
                pygame.draw.rect(win, LIGHT_GRAY, (self.x, self.y, SONGS_X + self.width, self.height))
        win.blit(self.message, (SONGS_X + self.x, self.y))

    def play(self, mouse_pos, event, song_list):
        if self.is_chosen(mouse_pos, event):
            global pause, song_index
            pause = False
            if not loop:
                song_index = self.index
            else:
                song_index = self.index - 1
            pygame.mixer.music.stop()
            pygame.mixer.music.load(f"{path}\\{self.name}")
            pygame.mixer.music.play()

def draw_playing_song(win):
    pygame.draw.rect(win, GREEN, (-10, song_index * SONG_BOX_SIZE, WIDTH + 10, SONG_BOX_SIZE), 2)

class Play_button(Button):
    def play(self, mouse_pos, event):
        global pause
        if self.is_ready(mouse_pos, event):
            if pause:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            pause = not pause

    def draw_sign(self, win):
        if pause:
            win.blit(play_image, (PLAY_BUTTON_X, PLAY_BUTTON_Y))
        else:
            win.blit(pause_image, (PLAY_BUTTON_X, PLAY_BUTTON_Y))           

class Replay_button(Button):
    def replay(self, mouse_pos, event):
        global pause
        if pygame.mixer.music.get_busy() or pause:
            if self.is_ready(mouse_pos, event):
                if not pygame.mixer.music.get_busy():
                    pause = not pause
                    pygame.mixer.music.unpause()
                pygame.mixer.music.set_pos(0.0)
                #pygame.mixer.music.rewind()

    def draw_sign(self, win):
        win.blit(replay_button_image, (REPLAY_BUTTON_X, REPLAY_BUTTON_Y))

class Mute_button(Button):
    def mute(self, mouse_pos, event):
        global is_muted
        if self.is_ready(mouse_pos, event):
            if is_muted:
                pygame.mixer.music.set_volume(1.0)
            else:
                pygame.mixer.music.set_volume(0.0)
            is_muted = not is_muted

    def draw_sign(self, win):
        if is_muted:
            win.blit(mute_button_on_image, (MUTE_BUTTON_X, MUTE_BUTTON_Y))
        else:
            win.blit(mute_button_off_image, (MUTE_BUTTON_X, MUTE_BUTTON_Y))

class Loop_button(Button):
    def loop(self, mouse_pos, event, song_list):
        global loop, song_index
        
        if self.is_ready(mouse_pos, event):
            loop = not loop
        if loop:
            if event.type == SONG_END:
                print('song has ended')
                if not (song_index >= len(song_list) - 1):
                    song_index += 1 
                else:
                    song_index = 0
                pygame.mixer.music.load(f"{path}\\{song_list[song_index]}")
                pygame.mixer.music.play()

    def draw_sign(self, win):
        if loop:
            win.blit(loop_button_on_image, (LOOP_BUTTON_X, LOOP_BUTTON_Y))
        else:
            win.blit(loop_button_off_image, (LOOP_BUTTON_X, LOOP_BUTTON_Y)) 

songs = []
for i in range(len(list_of_files)):
    songs.append(Song(list_of_files[i], i * SONG_BOX_SIZE + 1, i))
    Song.songs_num += 1

try:
    songs_on_screen = (HEIGHT - SLIDE_BAR_HEIGHT - CONTROL_BAR_HEIGHT) // songs[0].height
    for song in songs:
        song.next_y = song.prev_y - (Song.songs_num - songs_on_screen) * song.height
except IndexError:
    songs_on_screen = 0