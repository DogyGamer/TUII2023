import pygame
import math as m
import struct
from elements import Plotter, drawinfo, BLACK, BarPlot
import time
from KomsibUNIORReader import SerialReader, getPorogs

WIDTH = 1280
HEIGHT = 720
FPS = 30

reader = SerialReader()
reader.startThread()
maximum, minimum, porog1, porog2 = getPorogs(reader)
print(maximum, minimum, porog1, porog2)
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #, pygame.RESIZABLE)
pygame.display.set_caption("ТЮИИ")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Plotter1 = Plotter(WIDTH/3,HEIGHT/4,0,HEIGHT-HEIGHT/4, 20)
Plotter1 = Plotter(WIDTH/2.4, HEIGHT/4,   0   ,HEIGHT-HEIGHT/4, 1024, "Сырой сигнал", screen)
Plotter3 = Plotter(WIDTH/2.4, HEIGHT/4,WIDTH/2.4,HEIGHT-HEIGHT/4, 1024, "Отфильтрованный",screen, minimum, maximum, porog1, porog2, drawPorog=True)
Bar1 = BarPlot(WIDTH/6,HEIGHT,(WIDTH/2.4)*2,0, screen, minimum, maximum, porog1, porog2)
# Plotter2 = Plotter(WIDTH/3, HEIGHT/4,(WIDTH/3)*2,HEIGHT-HEIGHT/4, 1024, "sin", screen)
# Цикл игры

running = True
while running:
    # Держим цикл на правильной скорости


    delay = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            reader.close()

    # Обновление
    Plotter1.updateAllData(reader.data)
    Plotter3.updateAllData(reader.filt_data)
    Bar1.UpdateValue(reader.filt_data[-1])

    all_sprites.update()
    # for count in RESOLUTION:
    # Рендеринг
    screen.fill(BLACK)
    drawinfo(delay, round((time.time()*1000)-reader.last_data,2), reader.serialConnection.in_waiting ,screen)

    Bar1.update()
    Plotter1.update()
    Plotter3.update()

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()