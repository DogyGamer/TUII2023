import pygame
import math as m
import struct
from elements import Plotter, drawinfo, BLACK, BarPlot, ImageHidden
import time
from KomsibUNIORReader import SerialReader, getPorogs

WIDTH = 1280
HEIGHT = 720
FPS = 60

Timer = 5 

#Инициализация модуля для получения данных  
reader = SerialReader()
reader.startThread()
#Получение пороговых значений
maximum, minimum, porog1, porog2 = getPorogs(reader)
print(maximum, minimum, porog1, porog2)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ТЮИИ")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

#Инициализация всех граф элементов
Plotter1 = Plotter(WIDTH/2.4, HEIGHT/4,   0   ,HEIGHT-HEIGHT/4, 1024, "Сырой сигнал", screen)
Plotter3 = Plotter(WIDTH/2.4, HEIGHT/4,WIDTH/2.4,HEIGHT-HEIGHT/4, 1024, "Отфильтрованный",screen, minimum, maximum, porog1, porog2, drawPorog=True)
Bar1 = BarPlot(WIDTH/6,HEIGHT,(WIDTH/2.4)*2,0, screen, minimum, maximum, porog1, porog2)
Image1 = ImageHidden(WIDTH-(WIDTH/6), HEIGHT-(HEIGHT/4),  0, 0, screen)

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

    if(reader.filt_data[-1] > porog2):
        Image1.diselectAll()
        Image1.squares[0].selected = True
        # self.current_color = RED
    elif(reader.filt_data[-1] > porog1 and reader.filt_data[-1] < porog2):
        # self.current_color = YELLOW
        Image1.diselectAll()
        Image1.squares[1].selected = True
    else:
        # self.current_color = GREEN
        Image1.diselectAll()
        Image1.squares[2].selected = True

    all_sprites.update()
    # for count in RESOLUTION:
    # Рендеринг
    screen.fill(BLACK)
    drawinfo(delay, round((time.time()*1000)-reader.last_data,2), reader.serialConnection.in_waiting ,screen)

    Bar1.update()
    Plotter1.update()
    Plotter3.update()
    Image1.upadte()
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()