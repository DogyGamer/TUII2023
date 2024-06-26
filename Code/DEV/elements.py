import pygame
import time
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (204,204,0)
pygame.font.init()
font = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 18)
font3 = pygame.font.Font(None, 32)

class HidingSquare():
    def __init__(self, w,h,x,y,screen, color):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.selected = False
        
        self.start_timer = time.time()
        self.completed = True

    def update(self):
        if(not self.selected):
            self.start_timer = time.time()
        
        if(int(round(time.time() - self.start_timer)) >= 5):
            self.completed = True
           
        
        if(not self.completed):
            pygame.draw.rect(self.screen, self.getLighterColor(), pygame.Rect(self.x, self.y, self.w, self.h))
            if(self.selected):
                title = font3.render(str(round(5 - (time.time() - self.start_timer))), True, WHITE)
            else:
                title = font3.render(str(5), True, WHITE)

            t_rect = title.get_rect()
            self.screen.blit(title, (self.x+(self.w/2)-t_rect.centerx, self.y+(self.h/2)+t_rect.centery))

        if(self.selected):
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.x, self.y, self.w, self.h),5)
            
        
        
    def getLighterColor(self):
        return [self.color[0] - self.color[0]/6, self.color[1] - self.color[1]/6, self.color[2] - self.color[2]/6]

class ImageHidden():
    def __init__(self, w, h, x,y, screen):
        
        self.W = w 
        self.H = h 
        self.X = x 
        self.Y = y 
        self.screen = screen
        
        self.image = pygame.image.load("./image.png")
        self.im_W = self.image.get_rect().w 
        self.im_H = self.image.get_rect().h 
        self.mini = min(self.H/self.im_H, self.W/self.im_W)
        self.new_W = self.im_W * self.mini 
        self.new_H = self.im_H * self.mini 
        self.image = pygame.transform.scale(self.image, (int(self.new_W), int(self.new_H)))
        
        self.new_X = self.X + ((self.W - self.new_W)/2)
        self.new_Y = self.Y + ((self.H - self.new_H)/2)
        
        self.squares = []
        colors = [RED, YELLOW, GREEN]
        for i in range(1,4):
            if(self.H/self.im_H < self.W/self.im_W):
                self.squares.append(HidingSquare(self.new_W, self.new_H/3, self.new_X, self.new_Y+((self.new_H/3)*(i-1)), self.screen,colors[i-1]))
            else:
                self.squares.append(HidingSquare(self.new_W/3, self.new_H, self.new_X+((self.new_W/3)*(i-1)), self.new_Y, self.screen,colors[i-1]))
        
        self.current_state = 0
        
    def diselectAll(self):
        for sq in self.squares:
            sq.selected = False
    def upadte(self):   
        self.screen.blit(self.image, pygame.Rect(self.new_X, self.new_Y, self.new_W, self.new_H))
        for square in self.squares:
            square.update()
            
        self.squares[self.current_state].update()
        
            

class BarPlot():
    def __init__(self, w, h, x,y, screen, minimum=0, maximum=0, porog1=0, porog2=0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.screen = screen

        self.current_val = 50

        self.maximum = maximum
        self.minimum = minimum
        self.porog1 = porog1
        self.porog2 = porog2


        self.lmax = 0
        self.lmin = 0
        self.h2 = self.h-(self.h/10)
        self.max_window_y = self.y+(self.h/10)        
        
        self.current_color = WHITE

    def update(self):
        # Title
        title = font.render(str(round(self.current_val, 2)), True, self.current_color)
        t_rect = title.get_rect()
        self.screen.blit(title, (self.x+(self.w/2)-t_rect.centerx, self.y+(self.h/20)+t_rect.centery))

        # MainRect
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.x, self.y, self.w, self.h), 3)

        # Groups Rects
        srx = self.x+self.w/4 
        srw = self.w/2

        y1 = self.DataCords2XYCords(self.lmax)
        h1 = self.h-y1
        y2 = self.DataCords2XYCords(self.porog2)
        h2 = self.h-y2
        y3 = self.DataCords2XYCords(self.porog1)
        h3 = self.h-y3
        pygame.draw.rect(self.screen, RED, pygame.Rect(srx, y1, srw, h1))
        pygame.draw.rect(self.screen, YELLOW, pygame.Rect(srx, y2, srw, h2))
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(srx, y3, srw, h3))

        # Current Value Bar rect
        curr_y = self.DataCords2XYCords(self.current_val)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(srx+srw/4, curr_y, srw/2, self.h-curr_y))


        # Values Markers 
        lmintext = font2.render(str(round(self.lmin,2))+" -", True, WHITE)
        lmaxtext = font2.render(str(round(self.lmax,2))+" -", True, WHITE)
        porog1text = font2.render(str(round(self.porog1,2))+" -", True, WHITE)
        porog2text = font2.render(str(round(self.porog2,2))+" -", True, WHITE)

        self.screen.blit(lmaxtext, (srx-lmaxtext.get_rect().w, self.max_window_y))
        self.screen.blit(lmintext, (srx-lmintext.get_rect().w, (self.y+self.h)-lmintext.get_rect().h-4 ))

        self.screen.blit(porog1text, (srx-porog1text.get_rect().w, y3-lmintext.get_rect().centery ))
        self.screen.blit(porog2text, (srx-porog2text.get_rect().w, y2-lmintext.get_rect().centery ))

    def UpdateValue(self, value):
        self.current_val = value

        self.lmax = max(self.maximum, value)
        self.lmin = min(self.minimum,value)-10

        d = self.lmax-self.lmin+0.00000001
        self.k = self.h2 / d

        if(value > self.porog2):
            self.current_color = RED
        elif(value > self.porog1 and value < self.porog2):
            self.current_color = YELLOW
        else:
            self.current_color = GREEN

    def DataCords2XYCords(self, point):
        return (self.h2-((point-self.lmin) * self.k))+self.max_window_y
class Plotter():
    def __init__(self, w, h, x,y, res,title, screen, minimum=0, maximum=0, porog1=0, porog2=0, drawPorog=False ):
        
        
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.res = res
        self.title = title 
        self.screen = screen

        self.drawPorog = drawPorog

        self.k = 0

        self.data = [] #Массив для хранения данных в том виде в котором они приходят
        self.nicedata = [] #Массив для хранения данных приведеных к координатам на экране
        self.xs = [] #Массив для хранения координат по х для каждой точки
        
        self.lmin = 0 #Локальный минимум на графике
        self.lmax = 0 #Локальный максимум на графике

        self.maximum = maximum
        self.minimum = minimum
        self.porog1 = porog1
        self.porog2 = porog2

        for i in range(res):
            self.nicedata.append(0) 
            self.xs.append(x+((w/res)*i))

    def addPoint(self,value):
        self.data.append(value)
        self.data = self.data[-self.res:]
        self.lmax = max(self.maximum, max(self.data))
        self.lmin = -min(self.minimum,min(self.data))

        d = self.lmin+self.lmax+0.00000001
        self.k = self.h / d 

        for i in range(len(self.data)):
            self.nicedata[i] = self.DataCords2XYCords(self.data[i]) 
            
    def updateAllData(self, data):
        self.data = data
        self.data = self.data[-self.res:]

        self.lmax = max(self.maximum, max(self.data))
        self.lmin = -min(self.minimum,min(self.data))

        d = self.lmin+self.lmax+0.00000001
        self.k = self.h / d 

        for i in range(len(self.data)):
            self.nicedata[i] = self.DataCords2XYCords(self.data[i])

    def DataCords2XYCords(self, point):
        #Пересчитываются при добавлении каждой новой точки
        #lmin - локальный минимум текущего отрезка данных
        #lmax - локальный максимум текущего отрезка данных
        #k - коэффицент масштаба по формуле h / (lmin+lmax) 
         
        #Остаются неизменными
        #h - высота плоттера на экране
        #y - координата левого верхнего угла плоттера в окне программы
        
        
        #point - значение данных
        return (self.h-((self.lmin+point) * self.k))+self.y

    def update(self):
        # Нарисовать очертания плоттера
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.x,self.y,self.w,self.h))
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(self.x,self.y,self.w,self.h), 3)

        # Нарисовать сам график
        lines = []
        for i in range(len(self.nicedata)):
            lines.append([self.xs[i], self.nicedata[i]])

        pygame.draw.aalines(self.screen, BLUE, False, lines)

        if(self.drawPorog):
            pygame.draw.aaline(self.screen, RED, (self.x, self.DataCords2XYCords(self.maximum)), (self.x+self.w, self.DataCords2XYCords(self.maximum)),4)
            pygame.draw.aaline(self.screen, RED, (self.x, self.DataCords2XYCords(self.porog2)), (self.x+self.w, self.DataCords2XYCords(self.porog2)),4)
            pygame.draw.aaline(self.screen, YELLOW, (self.x, self.DataCords2XYCords(self.porog1)), (self.x+self.w, self.DataCords2XYCords(self.porog1)),4)
            pygame.draw.aaline(self.screen, GREEN, (self.x, self.DataCords2XYCords(self.minimum)), (self.x+self.w, self.DataCords2XYCords(self.minimum)),4)

        #Нарисовать максимальное и минимальное значение на графике 
        lmintext = font2.render("- "+str(round(-self.lmin,2)), True, BLACK)
        lmaxtext = font2.render("- "+str(round(self.lmax,2)), True, BLACK)
        self.screen.blit(lmaxtext, (self.x, self.y))
        self.screen.blit(lmintext, (self.x, (self.y+self.h)-lmintext.get_rect().h ))

        # Нарисовать заголовок
        title = font.render(self.title, True, BLACK)
        t_rect = title.get_rect()
        self.screen.blit(title, (self.x+(self.w/2)-t_rect.centerx,self.y+2))
        
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


def drawinfo(framedelay, datadelay,unreaded_data, screen):
    framedelay_text = font2.render("frame_delay: "+str(framedelay), True, WHITE)
    datadelay_text = font2.render("data_delay: "+str(datadelay), True, WHITE)
    unreaded_data_text = font2.render("unreaded_data: "+str(unreaded_data), True, WHITE)

    bottom = framedelay_text.get_rect().bottom+2

    screen.blit(framedelay_text, (0,0))
    screen.blit(datadelay_text, (0,bottom))
    screen.blit(unreaded_data_text, (0,bottom*2))