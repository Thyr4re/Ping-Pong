#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer
win_height = 500
win_widght = 700
window = display.set_mode((win_widght,win_height))
display.set_caption('Шутер')
backround= transform.scale(image.load('galaxy.jpg'),(win_widght,win_height))
window.blit(backround,(0,0))


FPS=60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

score1 = 0
lost = 0
life = 3
fireb = 10

font.init()
font1 = font.SysFont('Arial',20)
font2 = font.SysFont('Arial',50)
win = font2.render('YOU WIN!',True,(255,215,0))
lose = font2.render('YOU LOSE!',True,(255,0,0))


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets =sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT] and self.rect.x < 645:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15,15,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rectx = randint(80,win_widght-80)
            self.rect.y =0
            lost = lost + 1
            
class Asteroid(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y > win_height:
            self.rectx = randint(80,win_widght-80)
            self.rect.y =0
            

rocket =Player('rocket.png',250,win_height - 80,75,75,2)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(30, win_widght - 30), -40 , 80, 50, randint(1, 4))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Asteroid('asteroid.png',randint(30,win_widght-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)

reload_time = False

clock = time.Clock()
game =True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key  ==K_SPACE:
                if fireb > 0 and reload_time == False:
                    fire_sound.play()
                    fireb = fireb - 1
                    rocket.fire()
                if fireb == 0 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if finish != True:

        window.blit(backround,(0,0))
        monsters.update()
        bullets.update()
        rocket.update()
        asteroids.update()
        rocket.reset()
        monsters.draw(window)    
        asteroids.draw(window)               
        bullets.draw(window)
        score = font1.render('Счёт:'+ str(score1),1,(255,255,255))
        window.blit(score,(10,20))
        miss = font1.render('Пропущено: '+ str(lost),1,(255,255,255))
        window.blit(miss,(10,50))
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font1.render('Wait, reload...!',1,(150,0,0))
                window.blit(reload,(270,450))
            else:
                fireb = 10
                reload_time = False
                 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score1 = score1 + 1
            monster = Enemy('ufo.png', randint(80, win_widght - 80), -40, 75,75, randint(1, 5))
            monsters.add(monster)
            
        if score1 >= 10:
            finish = True
            window.blit(win,(230,250))
            
        if sprite.spritecollide(rocket, monsters , False) or sprite.spritecollide(rocket,asteroids,False):
            sprite.spritecollide(rocket,monsters, True)
            sprite.spritecollide(rocket,asteroids, True)
            life = life -1

        if life ==3:
            life_color=(0,150,0)
        if life ==2:
            life_color=(150,150,0)
        if life ==1:
            life_color=(150,0,0)
        lifes = font2.render(str(life),1,life_color)
        window.blit(lifes,(650,20))
        fireb1 = font2.render(str(fireb),1,(255,255,255))
        window.blit(fireb1,(640,440))
        
        if life ==0 or lost >=3:
            finish = True
            window.blit(lose,(230,250))

    display.update()
    clock.tick(FPS)