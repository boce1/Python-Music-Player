from utils.setings import *
from utils._path_ import list_of_files, path, make_default_path
from utils.button import *
import pygame
from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from mutagen.mp3 import MP3
import math

pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Consolas", font_size)

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
loop = False
loop_index = 0
loop_types = ("loop off", "loop", "loop one")
pause = False
is_muted = False
song_index = 0
start = True
is_replayed = False
is_song_skipped = False
volume = 1.0
temp_volume = volume

passed_seconds = 0

root = Tk()
root.withdraw()

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
                pygame.draw.rect(win, LIGHT_GRAY, (self.x, self.y, self.width + 2 * SONGS_X, self.height))
            else:
                pygame.draw.rect(win, LIGHT_GRAY, (self.x, self.y, 2 * SONGS_X + self.width, self.height))
        win.blit(self.message, (SONGS_X + self.x, self.y))

    def play(self, mouse_pos, event, song_list):
        if self.is_chosen(mouse_pos, event):
            global pause, song_index, start, passed_seconds
            pause = False
            if loop_types[loop_index] in ("loop off", "loop one") or start:
                song_index = self.index
                
            else:
                song_index = self.index - 1

            if start: # if is it start and loop is True then index will be index - 1 
                start = False # after start keep of the program songs_index = self.index - 1
            passed_seconds = 0
            pygame.mixer.music.stop()
            pygame.mixer.music.load(f"{path}\\{self.name}")
            pygame.mixer.music.play()


def mark_playing_song(win):
    if 0 < len(songs) and songs[song_index].y < SLIDE_BAR_Y:
        if not start:
            song = songs[song_index]
            if loop_types[loop_index] == "loop off":
                pygame.draw.rect(win, WHITE, (song.x, song.y, song.width + 2 * SONGS_X, song.height), 1)

def is_song_index_bigger_than_0():
    return len(list_of_files) > 0

playing_song_left = True
playing_song_x_ = SONGS_X
def show_playing_song(win):
    global playing_song_left, playing_song_x_
    if is_song_index_bigger_than_0():
        text = font.render(str(list_of_files[song_index].split(".mp3")[0]), True, BLACK)

    pygame.draw.rect(win, WHITE, (0, SONG_PLALYING_TEXT, WIDTH, SONG_PLALYING_TEXT_HEIGHT))
    if not start:
        if SONGS_X + text.get_width() < WIDTH:
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, SONG_PLALYING_TEXT + 1))
        else:
            win.blit(text, (playing_song_x_, SONG_PLALYING_TEXT + 1))
            if playing_song_left:
                playing_song_x_ -= 1
            if playing_song_x_ <= WIDTH - text.get_width():
                playing_song_left = False
            if not playing_song_left:
                playing_song_x_ += 1
            if playing_song_x_ >= SONGS_X:
                playing_song_left = True
    else:
        start_text = font.render("No song is playing", True, BLACK)
        win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, SONG_PLALYING_TEXT + 1))

class Play_button(Button):
    def play(self, mouse_pos, event):
        global pause
        if self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_SPACE):
            if pause:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

            if not start:
                pause = not pause

    def draw_sign(self, win):
        if pause:
            win.blit(play_image, (PLAY_BUTTON_X, PLAY_BUTTON_Y))
        else:
            win.blit(pause_image, (PLAY_BUTTON_X, PLAY_BUTTON_Y))           

class Replay_button(Button):
    def replay(self, mouse_pos, event):
        global pause, is_replayed
        if (self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_r)) and not start:
            if not pygame.mixer.music.get_busy():
                pause = False
                pygame.mixer.music.unpause()

            is_replayed = True
            if is_song_index_bigger_than_0():
                pygame.mixer.music.load(f"{path}\\{list_of_files[song_index]}")
                pygame.mixer.music.play()

        if self.is_relised(mouse_pos, event):
            is_replayed = False 

    def draw_sign(self, win):
        win.blit(replay_button_image, (REPLAY_BUTTON_X, REPLAY_BUTTON_Y))

class Mute_button(Button):
    def mute(self, mouse_pos, event):
        global is_muted, volume, temp_volume
        if self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_m):
            volume = pygame.mixer.music.get_volume()
            if volume > 0.0: 
                temp_volume = volume
            if is_muted:
                pygame.mixer.music.set_volume(temp_volume)

            else:
                pygame.mixer.music.set_volume(0.0)

        if pygame.mixer.music.get_volume() == 0.0:
            is_muted = True
        else:
            is_muted = False

    def draw_sign(self, win):
        if pygame.mixer.music.get_volume() == 0:
            win.blit(mute_button_on_image, (MUTE_BUTTON_X, MUTE_BUTTON_Y))
        else:
            win.blit(mute_button_off_image, (MUTE_BUTTON_X, MUTE_BUTTON_Y))


class Loop_button(Button):
    def song_ended(self, event):
        return event.type == SONG_END

    def play_song_q(self, song_list):
        global passed_seconds
        pygame.mixer.music.load(f"{path}\\{song_list[song_index]}")
        passed_seconds = 0
        pygame.mixer.music.play()

    def loop(self, mouse_pos, event, song_list):
        global loop_index, song_index
        if self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_l):
            loop_index += 1
            if loop_index >= len(loop_types):
                loop_index = 0

        if loop_types[loop_index] == "loop":
            if self.song_ended(event):
                if not (song_index >= len(song_list) - 1):
                    song_index += 1 
                else:
                    song_index = 0

                self.play_song_q(song_list)            

        if loop_types[loop_index] == "loop one":
            if self.song_ended(event):
                self.play_song_q(song_list)            

    def draw_sign(self, win):
        if loop_types[loop_index] == "loop":
            win.blit(loop_button_on_image, (LOOP_BUTTON_X, LOOP_BUTTON_Y))
        elif loop_types[loop_index] == "loop one":
            win.blit(loop_one_button_image, (LOOP_BUTTON_X, LOOP_BUTTON_Y))
        else:
            win.blit(loop_button_off_image, (LOOP_BUTTON_X, LOOP_BUTTON_Y)) 


class Forward_button(Button):
    def forward(self, mouse_pos, event, song_list):
        global song_index, pause, start, is_song_skipped 
        if self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_f):
            if not start:
                song_index += 1
                if song_index >= len(song_list):
                    song_index = 0

                if not pygame.mixer.music.get_busy() and pause:
                    pause = not pause

                start = False
                is_song_skipped = True

                if is_song_index_bigger_than_0():
                    pygame.mixer.music.load(f"{path}\\{song_list[song_index]}")
                    pygame.mixer.music.play()

        if self.is_relised(mouse_pos, event) or self.is_key_relised(event, pygame.K_f):
            is_song_skipped = False

    def draw_sign(self, win):
        win.blit(forwad_button_image, (FORWARD_BUTTON_X, FORWARD_BUTTON_Y))


class Backward_button(Button):
    def backward(self, mouse_pos, event, song_list):
        global song_index, pause, start, is_song_skipped
        if self.is_ready(mouse_pos, event) or self.is_key_pressed(event, pygame.K_b):
            if not start:
                song_index -= 1
                if song_index <= 0:
                    song_index = len(song_list) - 1

                if not pygame.mixer.music.get_busy() and pause:
                    pause = not pause

                start = False
                is_song_skipped = True

                if is_song_index_bigger_than_0():
                    pygame.mixer.music.load(f"{path}\\{song_list[song_index]}")
                    pygame.mixer.music.play()

        if self.is_relised(mouse_pos, event) or self.is_key_relised(event, pygame.K_b):
            is_song_skipped = False

    def draw_sign(self, win):
        win.blit(backward_button_image, (BACKWARD_BUTTON_X, BACKWARD_BUTTON_Y))


class Directory_button(Button):
    def chose_directory(self, mouse_pos, event):
        global pause 
        if self.is_ready(mouse_pos, event):
            pygame.mixer.music.pause()
            pause = True
            path = askdirectory()
            make_default_path(path)
            messagebox.showinfo("Music Player", "You need to restart the program if you want to play songs in the chosen location.")
        
    def draw_sign(self, win):
        win.blit(save_button_image, (SAVE_BUTTON_X, SAVE_BUTTON_Y))


class Progress_bar:
    x = SONGS_X
    y = SLIDE_BAR_Y
    width = WIDTH - 2 * x
    height = SLIDE_BAR_HEIGHT
    line_y = y + height // 2
    circle_x = x
    circle_radious = SONGS_X

    def duration(self):
        if is_song_index_bigger_than_0():
            audio = MP3(f"{path}\\{list_of_files[song_index]}")
            return audio.info.length
        return 1

    def is_mouse_pointing(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if Progress_bar.x <= mouse_x <= Progress_bar.x + Progress_bar.width and \
            Progress_bar.y <= mouse_y <= Progress_bar.y + Progress_bar.height:
            return True
        return False 

    def is_relised(self, mouse_pos, event):
        if self.is_mouse_pointing(mouse_pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                return True
        return False

    def draw_x(self, win, mouse_pos, mouse_button):
        if Progress_bar.circle_x != Progress_bar.x:
            if self.is_mouse_pointing(mouse_pos):
                if mouse_button[0]:
                    pygame.draw.circle(win, WHITE, (mouse_pos[0], Progress_bar.line_y), Progress_bar.circle_radious)
                    pygame.draw.circle(win, BLACK, (mouse_pos[0], Progress_bar.line_y), Progress_bar.circle_radious, 1)

    def change_time(self, mouse_pos, event):
        global passed_seconds
        if self.is_relised(mouse_pos, event):
            x = mouse_pos[0]
            width = Progress_bar.x + Progress_bar.width

            if x > Progress_bar.circle_x:
                passed_seconds += (x - Progress_bar.circle_x) / width * self.duration()
            else:
                passed_seconds -= (Progress_bar.circle_x - x) / width * self.duration()
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.set_pos(passed_seconds)

    def draw(self, win):
        global passed_seconds
        if not pause and not start:
            passed_seconds += 1 / FPS
        if is_replayed or is_song_skipped:
            passed_seconds = 0

        
        Progress_bar.circle_x = Progress_bar.x + Progress_bar.width * passed_seconds / self.duration()
        pygame.draw.line(win, GREEN, (Progress_bar.x, Progress_bar.line_y), (Progress_bar.x + Progress_bar.width, Progress_bar.line_y), 3)
        pygame.draw.line(win, BLACK, (Progress_bar.x, Progress_bar.line_y), (Progress_bar.x + Progress_bar.width, Progress_bar.line_y), 1)
        
        if pygame.mixer.music.get_pos() < 0 or Progress_bar.circle_x >= Progress_bar.x + Progress_bar.width:
            Progress_bar.circle_x = Progress_bar.x
            
        pygame.draw.circle(win, DARK_GREEN, (Progress_bar.circle_x, Progress_bar.line_y), Progress_bar.circle_radious)
        pygame.draw.circle(win, GREEN, (Progress_bar.circle_x, Progress_bar.line_y), Progress_bar.circle_radious, 1)

        if pygame.mixer.music.get_busy() or pause:
            minutes = int(passed_seconds // 60)
            seconds = int(passed_seconds % 60)
            if minutes >= 10:
                string_munites = str(minutes)
            else:
                string_munites = f"0{minutes}"
            if seconds >= 10:
                string_seconds = str(seconds)
            else:
                string_seconds = f"0{seconds}"

            if passed_seconds > self.duration():
                string_munites = "00"
                string_seconds = "00"
                
            time_string = f"{string_munites}:{string_seconds}"
            passed_seconds_message = font.render(time_string, True, WHITE)
        else:
            passed_seconds_message = font.render("00:00", True, WHITE)

        if not start:
            lenght_minutes = int(self.duration() // 60)
            lenght_seconds = int(self.duration() % 60)
            if lenght_minutes >= 10:
                lenght_minutes = str(lenght_minutes)
            else:
                lenght_minutes = f"0{lenght_minutes}"
            if lenght_seconds >= 10:
                lenght_seconds = str(lenght_seconds)
            else:
                lenght_seconds = f"0{lenght_seconds}"
            lenght_message = f"{lenght_minutes}:{lenght_seconds}"
            song_lenght = font.render(lenght_message, True, WHITE)
        else:
            song_lenght = font.render("00:00", True, WHITE)


        win.blit(passed_seconds_message, (LOOP_BUTTON_X - GAP - passed_seconds_message.get_width(), toolbar_button_y_position(passed_seconds_message.get_height())))
        win.blit(song_lenght, (FORWARD_BUTTON_X + FORWARD_BUTTON_SIZE + GAP, toolbar_button_y_position(passed_seconds_message.get_height())))

songs = []
for i in range(len(list_of_files)):
    songs.append(Song(list_of_files[i], i * SONG_BOX_SIZE + 1, i))
    Song.songs_num += 1

try:
    songs_on_screen = (HEIGHT - SLIDE_BAR_HEIGHT - CONTROL_BAR_HEIGHT - SONG_PLALYING_TEXT_HEIGHT) // songs[0].height
    for song in songs:
        song.next_y = song.prev_y - (Song.songs_num - songs_on_screen) * song.height
except IndexError:
    songs_on_screen = 0