from utils.setings import *
from utils._path_ import list_of_files, path
from utils.button import *
import pygame
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Consolas", font_size)

pause = False
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
            global pause
            pause = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load(f"{path}\\{self.name}")
            pygame.mixer.music.play()


class Play_button(Button):
    def play(self, mouse_pos, event):
        global pause
        if self.is_ready(mouse_pos, event):
            if pause:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            pause = not pause
                
class Replay_button(Button):
    def replay(self, mouse_pos, event):
        global pause
        if self.is_ready(mouse_pos, event):
            if not pygame.mixer.music.get_busy():
                pause = not pause
                pygame.mixer.music.unpause()
            pygame.mixer.music.rewind()


is_muted = False
class Mute_button(Button):
    def mute(self, mouse_pos, event):
        global is_muted
        if self.is_ready(mouse_pos, event):
            if is_muted:
                pygame.mixer.music.set_volume(1.0)
            else:
                pygame.mixer.music.set_volume(0.0)
            is_muted = not is_muted


songs = []
for i in range(len(list_of_files)):
    songs.append(Song(list_of_files[i], i * font_size + 1, i))
    Song.songs_num += 1

songs_on_screen = (HEIGHT - SLIDE_BAR_HEIGHT - CONTROL_BAR_HEIGHT) // songs[0].height
for song in songs:
    song.next_y = song.prev_y - (Song.songs_num - songs_on_screen) * song.height