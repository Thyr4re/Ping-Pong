from pygame import *

win_height = 700
win_widght = 900
window = display.set_mode((win_widght,win_height))
display.set_caption('Pin-Pong')
back=(173, 216, 230)
window.fill(back)

FPS=60
clock = time.Clock()
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

ball = GameSprite('Ball.png',350,350,50,50,4)
game =True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    ball.reset()

    display.update()
    clock.tick(FPS)
