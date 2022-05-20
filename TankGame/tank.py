import pygame, sys, random, time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

class Tank():
    def __init__(self):
        self.width = TANKWIDTH
        self.height = TANKHEIGHT
        self.x = width/2
        self.y = height - 42
        self.speed = speed
        self.angel = 90
        self.img = pygame.transform.rotate(png_tank, self.angel)
        self.surface = pygame.Surface((self.width, self.height))
    def draw(self):
        screen.blit(self.img, (int(self.x), int(self.y)))
    def update(self, moveLeft, moveRight, moveUp, moveDown):
        original_x = self.x
        original_y = self.y
        if moveLeft == True:
            self.x -= self.speed
            self.angel = 180
            self.img = pygame.transform.rotate(png_tank, self.angel)
        if moveRight == True:
            self.x += self.speed
            self.angel = 0
            self.img = pygame.transform.rotate(png_tank, self.angel)
        if moveUp == True:
            self.y -= self.speed
            self.angel = 90
            self.img = pygame.transform.rotate(png_tank, self.angel)
        if moveDown == True:
            self.y += self.speed
            self.angel = 270
            self.img = pygame.transform.rotate(png_tank, self.angel)
        if self.x<0 or self.x>width-self.width or self.y<0 or self.y>height-self.height:
            self.x = original_x
            self.y = original_y
        index = 0
        countR = 0
        for i_wall in walls:
            if (rectCollision((self.x, self.y,self.width,self.height), i_wall)):
                countR += 1
        if countR != 0:
            self.x = original_x
            self.y = original_y
    def get_angel(self):
        return self.angel
    def get_vitri(self):
        return (int(self.x+17) , int(self.y+17))

class Tank_enemy():
    def __init__(self):
        self.width = TANKWIDTH
        self.height = TANKHEIGHT
        self.x = vtri*100
        self.y = 0
        self.speed = speed
        self.angel = 270
        self.img = pygame.transform.rotate(png_tank_enemy, self.angel)
        self.surface = pygame.Surface((self.width, self.height))
    def draw(self):
        screen.blit(self.img, (int(self.x), int(self.y)))
    def update(self, moveLeft, moveRight, moveUp, moveDown):
        original_x = self.x
        original_y = self.y
        if moveLeft == True:
            self.x -= self.speed
            self.angel = 180
            self.img = pygame.transform.rotate(png_tank_enemy, self.angel)
        if moveRight == True:
            self.x += self.speed
            self.angel = 0
            self.img = pygame.transform.rotate(png_tank_enemy, self.angel)
        if moveUp == True:
            self.y -= self.speed
            self.angel = 90
            self.img = pygame.transform.rotate(png_tank_enemy, self.angel)
        if moveDown == True:
            self.y += self.speed
            self.angel = 270
            self.img = pygame.transform.rotate(png_tank_enemy, self.angel)
        if self.x<0 or self.x>width-self.width or self.y<0 or self.y>height-self.height:
            self.x = original_x
            self.y = original_y
        index = 0
        countR = 0
        for i_wall in walls:
            if (rectCollision((self.x, self.y,self.width,self.height), i_wall)):
                countR += 1
        if countR != 0:
            self.x = original_x
            self.y = original_y
    def get_angel(self):
        return self.angel
    def get_vitri(self):
        return (int(self.x+17) , int(self.y+17))

#Dinh dang map
bg = pygame.image.load('images/grass2.png')
wall = pygame.image.load('images/block.png')
walls=[]
for x in range(16):
    for y in range(10):
        if random.randint(0,100) < 50:
            x_wall = x * 50
            y_wall = y * 50 + 50
            xl_wall = 50
            yl_wall = 50
            walls.append((x_wall, y_wall, xl_wall, yl_wall))

#Dinh dang xe tank
png_tank = pygame.image.load('images/tank_sand.png')
TANKWIDTH = 40
TANKHEIGHT = 40
speed = 3
png_bullet_tank = pygame.image.load('images/bulletsand2.png')
bullets=[]
bullet_delay = 0
bullet_wall = pygame.mixer.Sound('sounds/gun9.wav')
YouWin = False

#Dinh dang xe tank dich
png_tank_enemy = pygame.image.load('images/tank_dark.png')
TANKWIDTH = 40
TANKHEIGHT = 40
speed = 3
png_bullet_tank_enemy = pygame.image.load('images/bulletdark2.png')
bullets_enemy=[]
bullet_delay_enemy = 0
enemy_move_count = 40
bullet_wall_enemy = pygame.mixer.Sound('sounds/gun10.wav')
bullet_tank = pygame.mixer.Sound('sounds/exp.wav')
 
#Ham dinh dang dan xe tank
def tank_bullet_set(bandan, angel, vitri):
    global bullet_delay      
    if bandan:
        if bullet_delay == 0:
            bullets.append((angel, vitri))
            bullet_delay = 20
        else:
            bullet_delay -=1
    for i in range(len(bullets)):
        if bullets[i][0] == 0:
            bullets[i] = (bullets[i][0], (bullets[i][1][0]+5,bullets[i][1][1]))
        if bullets[i][0] == 180:
            bullets[i] = (bullets[i][0], (bullets[i][1][0]-5,bullets[i][1][1]))
        if bullets[i][0] == 90:
            bullets[i] = (bullets[i][0], (bullets[i][1][0],bullets[i][1][1]-5))
        if bullets[i][0] == 270:
            bullets[i] = (bullets[i][0], (bullets[i][1][0],bullets[i][1][1]+5))
    for i in range(len(bullets)):
        kt = False
        for w in range(len(walls)):
            if rectCollision((bullets[i][1][0],bullets[i][1][1],10,10),walls[w]):
                bullet_wall.play()
                del walls[w]
                del bullets[i]
                kt = True
                break
        if kt:
            break       
        if bullets[i][1][0]<0 or bullets[i][1][0]>width or bullets[i][1][1]<0 or bullets[i][1][1]>height:
            del bullets[i]
            break
        for e in range(len(tank_enemys)):
            vtp = tank_enemys[e].get_vitri()
            if rectCollision((bullets[i][1][0],bullets[i][1][1],10,10),(vtp[0],vtp[1],42,42)):
                bullet_tank.play()
                del bullets[i]
                del tank_enemys[e]
                kt = True
                break       
        if kt:
            break  

def tank_bullet_enemy_set():
    for i in range(len(bullets_enemy)):
        if bullets_enemy[i][0] == 0:
            bullets_enemy[i] = (bullets_enemy[i][0], (bullets_enemy[i][1][0]+5,bullets_enemy[i][1][1]))
        if bullets_enemy[i][0] == 180:
            bullets_enemy[i] = (bullets_enemy[i][0], (bullets_enemy[i][1][0]-5,bullets_enemy[i][1][1]))
        if bullets_enemy[i][0] == 90:
            bullets_enemy[i] = (bullets_enemy[i][0], (bullets_enemy[i][1][0],bullets_enemy[i][1][1]-5))
        if bullets_enemy[i][0] == 270:
            bullets_enemy[i] = (bullets_enemy[i][0], (bullets_enemy[i][1][0],bullets_enemy[i][1][1]+5))
    for i in range(len(bullets_enemy)):
        kt = False
        for w in range(len(walls)):
            if rectCollision((bullets_enemy[i][1][0],bullets_enemy[i][1][1],10,10),walls[w]):
                bullet_wall_enemy.play()
                del walls[w]
                del bullets_enemy[i]
                kt = True
                break        
        if kt:
            break
        if bullets_enemy[i][1][0]<0 or bullets_enemy[i][1][0]>width or bullets_enemy[i][1][1]<0 or bullets_enemy[i][1][1]>height:
            del bullets_enemy[i]
            break  
    
def gamePlay(tank, tank_enemys):
    global png_tank, enemy_move_count, bullet_delay_enemy
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    bandan = False
    while gameOver(tank):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT and  moveRight == False and moveUp == False and moveDown == False:
                    moveLeft = True
                if event.key == K_RIGHT and  moveLeft == False and moveUp == False and moveDown == False:
                    moveRight = True
                if event.key == K_UP and  moveRight == False and moveLeft == False and moveDown == False:
                    moveUp = True                  
                if event.key == K_DOWN and  moveRight == False and moveUp == False and moveLeft == False:
                    moveDown = True
                if event.key == K_SPACE:
                    bandan = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
                if event.key == K_SPACE:
                    bandan = False
      
        screen.blit(bg, (0, 0))
        for i_wall in walls:
            screen.blit(wall, (i_wall[0], i_wall[1]))
        tank_bullet_set(bandan, tank.get_angel(), tank.get_vitri())
        for i_bullet in bullets:
            img = pygame.transform.rotate(png_bullet_tank, i_bullet[0])
            screen.blit(img, i_bullet[1])
        tank.draw()
        tank.update(moveLeft, moveRight, moveUp, moveDown)
        for tank_enemy in tank_enemys:
            choice_enemy = random.randint(0, 3)
            if enemy_move_count > 0:
                enemy_move_count -= 1
                if tank_enemy.get_angel() == 0:
                    tank_enemy.update(False, True, False, False)
                if tank_enemy.get_angel() == 90:
                    tank_enemy.update(False, False, True, False)
                if tank_enemy.get_angel() == 180:
                    tank_enemy.update(True, False, False, False)
                if tank_enemy.get_angel() == 270:
                    tank_enemy.update(False, False, False, True)
            if choice_enemy == 0:
                enemy_move_count = 30
            elif choice_enemy == 1:
                ra = random.randint(0, 3)
                if ra == 0:
                    tank_enemy.update(False, True, False, False)
                if ra == 1:
                    tank_enemy.update(False, False, True, False)
                if ra == 2:
                    tank_enemy.update(True, False, False, False)
                if ra == 3:
                    tank_enemy.update(False, False, False, True)
            elif choice_enemy == 2:
                if bullet_delay_enemy == 0:
                    bullets_enemy.append((tank_enemy.get_angel(), tank_enemy.get_vitri()))
                    bullet_delay_enemy = 20
                else:
                    bullet_delay_enemy -=1
        tank_bullet_enemy_set()
        for i_bullet in bullets_enemy:
            img = pygame.transform.rotate(png_bullet_tank_enemy, i_bullet[0])
            screen.blit(img, i_bullet[1])
        for i in tank_enemys:
            i.draw()
        pygame.display.update() 
        clock.tick(60)

def gameOver(tank):
    global YouWin
    if len(tank_enemys) == 0:
        bgGO = pygame.image.load('game_over/game_win.jpg')
        screen.blit(bgGO,(0,0))
        pygame.display.update()
        time.sleep(3)
        return False
    for i in range(len(bullets_enemy)):
        vt = tank.get_vitri()
        if rectCollision((vt[0],vt[1],42,42),(bullets_enemy[i][1][0],bullets_enemy[i][1][1],10,10)):
            bgGO = pygame.image.load('game_over/game_over.jpg')
            screen.blit(bgGO,(0,0))
            pygame.display.update()
            time.sleep(3)
            return False
    return True

tank = Tank()
tank_enemys = []
vtri = 0
for i in range(6):
    vtri = i
    tank_enemys.append(Tank_enemy())

gamePlay(tank, tank_enemys)