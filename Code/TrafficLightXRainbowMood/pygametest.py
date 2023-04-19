# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import math as m
import struct
from elements import Plotter, drawframedelay, BLACK

# 1 24 = 84
# 6 13 = 373


WIDTH = 1280
HEIGHT = 720
FPS = 60

d = open("3ds.txt", "rb")

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #, pygame.RESIZABLE)
pygame.display.set_caption("ТЮИИ")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Plotter1 = Plotter(WIDTH/3,HEIGHT/4,0,HEIGHT-HEIGHT/4, 20)
Plotter1 = Plotter(WIDTH/3,HEIGHT/4,0,HEIGHT-HEIGHT/4, 1000, "raw signal", screen)
Plotter3 = Plotter(WIDTH/3, HEIGHT/4,WIDTH/3,HEIGHT-HEIGHT/4, 1000, "filtered", screen)
Plotter2 = Plotter(WIDTH/3, HEIGHT/4,(WIDTH/3)*2,HEIGHT-HEIGHT/4, 100, "sin", screen)
# Цикл игры
running = True
counter = 0

WINDOWLENGTH = 75

data = []
absdata = []
filtdata = []

delaycounter = 0

while running:
    # Держим цикл на правильной скорости
    counter +=1
    read = d.read(4)
    if(read == b"DATA"):
        d.read(12)
    else:
        delaycounter += 1
        value = round(struct.unpack("f", read)[0])
        if not (value > 1000 or value < -1000):
            data.append(value)
            absdata.append(abs(value))
            filtdata.append(sum(absdata[-WINDOWLENGTH:]) / WINDOWLENGTH)
            Plotter1.addPoint(value)
            Plotter3.addPoint(filtdata[-1])

    if(delaycounter <= 4):
        continue

    delaycounter = 0
    
    Plotter2.addPoint(abs(m.sin(2*counter)*m.sin(counter/10)*m.cos(3*counter)*800))
    

    delay = clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            pass
            # Plotter1.sizeChanged(event.size)
            # Plotter2.sizeChanged(event.size)

    # Обновление
        
     
    all_sprites.update()
    # for count in RESOLUTION:
    # Рендеринг
    screen.fill(BLACK)
    drawframedelay("delay: "+str(delay), screen)
    Plotter1.update()
    Plotter2.update()
    Plotter3.update()
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()