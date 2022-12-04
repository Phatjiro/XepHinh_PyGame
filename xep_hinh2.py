#nguyenvanphat
from types import coroutine
import pygame as pg
import random as ran
from dataclasses import dataclass
pg.init()
width, columns, rows = 360, 12, 22
distance = width // columns # 300/10 = 30
height = distance * rows
grid = [0] * (columns+6) * (rows+4)
#print(grid)
speed, score, flag_score, sound_score, level, precent_level, temp = 800, 0, 500, 0, 1, 0, 0
high_score = 0
a = 0

with open("high_score.txt") as f:
    for line in f:
        pass
    last_line = line
# print(last_line)

high_score = int(last_line)

# load hình 
picture = []
for n in range(8):
    picture.append(pg.transform.scale(pg.image.load(f'T_{n}.jpg'), (distance, distance)))
# screen = pg.display.set_mode([width, height])
# pg.display.set_caption('Game xếp hình - Phatjiro')

# nền
background = pg.image.load('board_tetris_ver3.png')
background_ngoai = pg.image.load('board_ngoai3.png')
#âm thanh
sound1 = pg.mixer.Sound('sound1.mp3')
sound1.set_volume(0.2)
sound2 = pg.mixer.Sound('sound2.mp3')
sound2.set_volume(0.4)
sound3 = pg.mixer.Sound('song_gameover.mp3')
sound3.set_volume(0.5)
sound_song1 = pg.mixer.Sound('tetris_song1.mp3')
sound_song1.set_volume(0.3)
sound_song2 = pg.mixer.Sound('tetris_song2.mp3')
sound_song2.set_volume(0.3)
sound_song3 = pg.mixer.Sound('tetris_song3_piano.mp3')
sound_song3.set_volume(0.5)
check_sound3 = 0

tetroromino_down = pg.USEREVENT+1
pg.time.set_timer(tetroromino_down, speed)

# tetroromino cho các hình gạch để xếp O,I,J,L,S,Z,T
tetroromino = [[0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0], #chữ O
                [0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0], #chữ I
                [0,0,0,0,3,3,3,0,0,0,3,0,0,0,0,0], #chữ J
                [0,0,4,0,4,4,4,0,0,0,0,0,0,0,0,0], #chữ L
                [0,5,5,0,5,5,0,0,0,0,0,0,0,0,0,0], #chữ S
                [6,6,0,0,0,6,6,0,0,0,0,0,0,0,0,0], #chữ Z
                [0,0,0,0,7,7,7,0,0,7,0,0,0,0,0,0]] #chữ T

#tạo lớp và định nghĩa hàm
@dataclass
class tetro():
    tetro : list
    row : int = 4
    column : int = 4 #vị trí xuất hiện lần đầu tiên

    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n % 4) * distance
                y = (self.row + n // 4) * distance
                screen.blit(picture[color],(x,y))

    def show_next(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n % 4 + 9) * distance
                y = (self.row + n // 4 + 2) * distance
                screen.blit(picture[color],(x,y))

    #check đụng tường
    def checkmove(self,r,c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                rs = r + n // 4
                cs = c + n % 4
                if cs < 0 or rs >= rows + 4 or cs >= columns or grid[rs * columns + cs] > 0:
                    return False
        return True

    def checkGameOver(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                y = (self.row + n // 4)
                if y == 4 and self.checkmove(self.row + 1, self.column + 0) == False:
                    return True
        return False                    

    #tạo hàm update vị trí cho hình
    def update(self,r,c):
        if self.checkmove(self.row + r, self.column + c) == True:
            self.row += r
            self.column += c
            return True
        return False

    #tạo hàm xoay cho hình
    def rotate(self):
        savetetro = self.tetro.copy()
        for n, color in enumerate(savetetro):
            self.tetro[(2 - (n % 4 )) * 4 + (n // 4)] = color
        if not self.checkmove(self.row, self.column):
            self.tetro = savetetro.copy()  

def ObjectOnGridLine():
    for n, color in enumerate(character.tetro):
        if color > 0:
            grid[(character.row + n // 4) * columns + (character.column + n % 4)] = color #kiểm tra đụng grid line để tạo hình mới

def DeleteAllRows():
    fullrows = 0
    for row in range(rows+4):
        for column in range(columns):
            if grid[row * columns + column] == 0:
                break
        else:
            del grid[row * columns : row * columns + columns]
            grid[0:0] = [0] * columns
            fullrows += 1
    return fullrows ** 2 * 100  

def DeleteAllGrid():
    for row in range(rows+4):
        for column in range(columns):
            del grid[row * columns : row * columns + columns]
            grid[0:0] = [0] * columns

character = tetro(ran.choice(tetroromino).copy())
# character = tetro(tetroromino[1])
next_character = tetro(ran.choice(tetroromino).copy())

screen = pg.display.set_mode([width+180,height+120]) #tạo màn hình
title = pg.display.set_caption('Game xếp hình - PhatJiro') #tạo tiêu đề
pg.display.set_icon(picture[2]) #set icon 

pausing = False
gameover = False
music = False

running = True #biến chạy cho chương trình

while running == True: #vòng lặp để chạy
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT: #tạo nút tắt để thoát vòng lặp
            running = False
        if event.type == tetroromino_down:
            if character.update(1,0) == False:
                ObjectOnGridLine()
                character = next_character
                next_character = tetro(ran.choice(tetroromino).copy())
                # character = tetro(tetroromino[1])
                score += DeleteAllRows()
                if score > sound_score:
                    pg.mixer.Sound.play(sound2)
                    sound_score = score

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                character.update(0,-1)
                pg.mixer.Sound.play(sound1)
            if event.key == pg.K_RIGHT:
                character.update(0,1)
                pg.mixer.Sound.play(sound1)
            if event.key == pg.K_DOWN:
                character.update(1,0)
                pg.mixer.Sound.play(sound1)
            if event.key == pg.K_SPACE:
                while character.update(1,0) == True:
                    a = 1
                pg.mixer.Sound.play(sound1)
            if event.key == pg.K_UP or event.key == pg.K_c:
                character.rotate()
                character.rotate()
                character.rotate()
                pg.mixer.Sound.play(sound1)
            if gameover == True:
                tetroromino_down = pg.USEREVENT+1
                speed, score, flag_score, sound_score, level, precent_level, temp = 800, 0, 500, 0, 1, 0, 0
                tuychinh1 = 22
                tuychinh2 = 22
                pg.time.set_timer(tetroromino_down, speed)
                DeleteAllGrid()
                check_sound3 = 0
                gameover = False
            if event.key == pg.K_p or event.key == pg.K_t:
                if pausing == False:
                    tetroromino_down = 0
                    pg.mixer.pause()
                    pausing = True
                    break
                if pausing == True:
                    tetroromino_down = pg.USEREVENT+1
                    pg.time.set_timer(tetroromino_down, speed)
                    pg.mixer.unpause()
                    pausing = False
                    break
            if event.key == pg.K_1:
                if music == False:
                    pg.mixer.Sound.play(sound_song1)
                    sound_song1.set_volume(0.3)
                    music = True
                    break
                if music == True:
                    pg.mixer.pause()
                    music = False
                    break
            if event.key == pg.K_2:
                if music == False:
                    pg.mixer.Sound.play(sound_song2)
                    sound_song2.set_volume(0.3)
                    music = True
                    break
                if music == True:
                    pg.mixer.pause()
                    music = False
                    break
            if event.key == pg.K_3:
                if music == False:
                    pg.mixer.Sound.play(sound_song3)
                    sound_song3.set_volume(0.5)
                    music = True
                    break
                if music == True:
                    pg.mixer.pause()
                    music = False
                    break

    if score >= flag_score:
        level = (score // 500) + 1
        flag_score += 500
        if level > precent_level:
            speed = int(speed * 0.8 ** (level - precent_level))
            pg.time.set_timer(tetroromino_down,speed)
            precent_level = level

    # screen.fill((50,50,50))
    screen.blit(background_ngoai,(0,0))
    screen.blit(background, (0,0+120))
    character.show()
    next_character.show_next()
    textsurface_nextShape = pg.font.Font('FVF_Fernando_08.ttf', 24).render('Tiếp theo', False, (0,0,0))
    screen.blit(textsurface_nextShape,(380,114))

    textsurface1 = pg.font.Font('FVF_Fernando_08.ttf', 24).render(f'Điểm', False, (0,0,0))
    screen.blit(textsurface1,(380,162+120))
    textsurface1_score = pg.font.Font('FVF_Fernando_08.ttf', 28).render(f'{score}', False, (255,255,200))
    screen.blit(textsurface1_score,(380,234+120))

    textsurface3 = pg.font.Font('FVF_Fernando_08.ttf', 24).render(f'Kỉ lục', False, (0,0,0))
    screen.blit(textsurface3,(384,324+120))
    textsurface3_highscore = pg.font.Font('FVF_Fernando_08.ttf', 28).render(f'{high_score}', False, (255,255,200))
    screen.blit(textsurface3_highscore,(380,400+120))

    textsurface2 = pg.font.Font('FVF_Fernando_08.ttf', 24).render(f'Cấp độ', False, (0,0,0))
    screen.blit(textsurface2,(380,488+120))
    textsurface2_level = pg.font.Font('FVF_Fernando_08.ttf', 28).render(f'{level}', False, (255,255,200))
    screen.blit(textsurface2_level,(380,565+120))

    textsurface_title = pg.font.Font('FVF_Fernando_08.ttf', 42).render('Xếp Hình', False, (0,0,0))
    screen.blit(textsurface_title,(150,0))

    textsurface_name = pg.font.Font('FVF_Fernando_08.ttf', 22).render('- PhatJiro -', False, (0,0,0))
    screen.blit(textsurface_name,(186,75))

    #load hình lên lưới
    for n, color in enumerate(grid):
        if color > 0:
            x = n % columns * distance
            y = n // columns * distance
            screen.blit(picture[color],(x,y))

    if character.checkGameOver() == True:
        gameover = True
        textsurface0 = pg.font.Font('FVF_Fernando_08.ttf', 36).render('Game Over!', False, (255,255,255))
        textsurface_reset = pg.font.Font('FVF_Fernando_08.ttf', 22).render('Nhấn bất kì để chơi lại', False, (255,255,200))
        screen.blit(textsurface0,(50,220+120))
        screen.blit(textsurface_reset,(30,300+120))
        tetroromino_down = 0
        if score > high_score:
            high_score = score
            with open("high_score.txt", "a") as file:
	            file.write(str(high_score) + "\r")
        if check_sound3 == 0:
            pg.mixer.Sound.play(sound3)
            check_sound3 = 1

    if pausing == True:
        textsurface_tam = pg.font.Font('FVF_Fernando_08.ttf', 36).render('Helluuuu!', False, (255,255,255))
        textsurface_tieptuc = pg.font.Font('FVF_Fernando_08.ttf', 22).render('Yêu Ngân 3000 :3', False, (255,255,200))
        screen.blit(textsurface_tam,(60,220+120))
        screen.blit(textsurface_tieptuc,(50,300+120))

    pg.display.flip()
pg.quit()
