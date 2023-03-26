from pygame import *

win_height = 700
win_widght = 900
window = display.set_mode((win_widght,win_height))
display.set_caption('Pin-Pong')
back=(173, 216, 230)
window.fill(back)



FPS=60

clock = time.Clock()
game =True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    

      

    display.update()
    clock.tick(FPS)
