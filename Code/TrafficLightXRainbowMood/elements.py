import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.font.init()
font = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 18)

class Plotter():
    def __init__(self, w, h, x,y, res,title, screen):
        
        
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.res = res
        self.title = title 
        self.screen = screen

        self.data = [] #Массив для хранения данных в том виде в котором они приходят
        self.nicedata = [] #Массив для хранения данных приведеных к координатам на экране
        self.xs = [] #Массив для хранения координат по х для каждой точки
        
        self.lmin = 0 #Локальный минимум на графике
        self.lmax = 0 #Локальный максимум на графике

        for i in range(res):
            self.nicedata.append(0) 
            self.xs.append(x+((w/res)*i))

    def addPoint(self,value):
        self.data.append(value)
        self.data = self.data[-self.res:]
        self.lmax = max(self.data)
        self.lmin = -min(self.data)

        d = self.lmin+self.lmax+0.00000001
        k = self.h / d 

        for i in range(len(self.data)):
            self.nicedata[i] = (self.h-((self.lmin+self.data[i]) * k))+self.y
            
    def update(self):
        # Нарисовать очертания плоттера
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.x,self.y,self.w,self.h))
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(self.x,self.y,self.w,self.h), 3)

        # Нарисовать заголовок
        title = font.render(self.title, True, WHITE)
        t_rect = title.get_rect()
        self.screen.blit(title, (self.x+(self.w/2)-t_rect.centerx,self.y-t_rect.height))

        # Нарисовать сам график
        lines = []
        for i in range(len(self.nicedata)):
            lines.append([self.xs[i], self.nicedata[i]])

        pygame.draw.aalines(self.screen, BLUE, False, lines)

        #Нарисовать максимальное и минимальное значение на графике 
        lmintext = font2.render("- "+str(round(-self.lmin,2)), True, BLACK)
        lmaxtext = font2.render("- "+str(round(self.lmax,2)), True, BLACK)
        self.screen.blit(lmaxtext, (self.x, self.y))
        self.screen.blit(lmintext, (self.x, (self.y+self.h)-lmintext.get_rect().h ))


        
class Point(pygame.sprite.Sprite):
    def __init__(self, x,y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2*radius, 2*radius))
        self.image.fill(RED)
        pygame.draw.circle(self.image, RED, (radius,radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x+radius,self.y+radius)
        
        
    def update(self):
        pass
        self.rect.center = (self.x+self.radius,self.y+self.radius)


def drawframedelay(text, screen):
    title = font2.render(text, True, WHITE)
    screen.blit(title, (0,0))
