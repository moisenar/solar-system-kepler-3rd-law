import pygame
from pygame.locals import *
import time
import math
import numpy as np
windowW = 1200
windowH = 800
Divfac = 100
movfac = 50

oney = 3600 * 24 * 365

Radifac = 3.6e-12
#sizefac = 7.4e-6
sizefac = 3.6e-6
timefac =  1#31536000
running = True

SunM = 1.98e30
SunS = 696340e-2
#MERCURY 	 VENUS 	 EARTH 	 MARS 	 JUPITER 	 SATURN 	 URANUS 	 NEPTUNE 	 PLUTO 
Masses = [0.33e24, 4.87e24 ,5.97e24 ,0.64e24 ,1898e24,568e24,86.8e24,102e24,0.0130e24] 

Radiis = [57.9e9,	108.2e9,	149.6e9,	228.0e9,	778.5e9,	1432.0e9,	2867.0e9,	4515.0e9,	5906.4e9]

sizes = [4879,	12104,	12756,	6792,	142984	,120536	,51118	,49528	,2376 ]

A0 = [ 0, 0 , 0 , 0 , 0 , 0 , 0, 0, 0]
RorL = [1 , -1 , 1 , 1 , 1 , 1 ,-1,1,1]
G = 6.67e-11




class Position2d:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

class Rotator:
    def __init__(self,Radius,P,A0,t,RorL):
        A0 = A0 / 180 * math.pi
        omega = 2*math.pi / P
        if RorL == 1:
            X2 = Radius * math.cos(A0 + omega*t) 
            Y2 = Radius * math.sin(A0 + omega*t)
        elif RorL == -1:
            X2 = Radius * math.cos(A0 - omega*t) 
            Y2 = Radius * math.sin(A0 - omega*t)
        else : 
            print("invalid input RorL")
        self.X2 = X2
        self.Y2 = Y2
   
     

def PCal (m1 , m2 , Radius): #created by mohsen ardalan
        
        P = 4 * math.pi * math.pi  * Radius *Radius *Radius / (G * (m1 +m2))
        return math.sqrt(P)
    


    

class topixel :
    Divfac = 0
    movfac = 0
    movR = 0
    movU = 0
    def __init__(self, Divfac , movfac  ):
        self.Divfac = Divfac
        self.movfac = movfac
    

    def Dis(self ,Dis) :
        return Dis * self.Divfac 
    def movup(self ,pix):
        self.movU += pix * self.movfac
    def movri(self ,pix):
        self.movR += pix * self.movfac
    def movori(self):
        self.movR = 0
        self.movU = 0
    def coorx (self , x): 
        return windowW / 2 + x * self.Divfac + self.movR
    def coory (self , y): 
        return windowH / 2 - y * self.Divfac + self.movU
        
px = topixel(Divfac ,movfac )


pygame.init()
window = pygame.display.set_mode((windowW , windowH))
window.fill((37, 41, 41))

t = 0
dt = 0
startt = time.time() 
endt = 0
font = pygame.font.Font('freesansbold.ttf', 32)


while running:
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_2:
                print(dt)
                timefac *= 10
            if event.key == pygame.K_1:
                timefac *= 0.1
                print(dt)
            if event.key == pygame.K_KP_PLUS:
                Radifac *= 1.1
                sizefac *= 1.1
            if event.key == pygame.K_KP_MINUS:
                
                Radifac *= 0.9
                sizefac *= 0.9
            if event.key == pygame.K_w:
                px.movup(1) 
            if event.key == pygame.K_s:
                px.movup(-1) 
            if event.key == pygame.K_a:
                px.movri(1) 
            if event.key == pygame.K_d:
                px.movri(-1) 
            if event.key == pygame.K_SPACE:
                px.movori()
    window.fill((37, 41, 41))
    

    D3 = px.Dis(SunS * sizefac)
    pygame.draw.circle(window, (168, 83, 62),
        [px.coorx(0),px.coory(0)], D3, 0)
    endt = time.time()
    dt = endt - startt 
    #print(dt)
    startt = time.time()
    
    t = t + dt* timefac

    text = font.render('time : ' + str(f'{t/ oney:.9f}' ) + " years", True, (107, 176, 194) ,)

    for i in range(0 , len(Masses)) :
            P = PCal(Masses[i] , SunM ,Radiis[i])
            print(P / (3600 * 24 * 365) )
            P1 = Rotator(Radiis[i] * Radifac ,P ,A0[i] , t ,RorL[i] )

            D1 = px.Dis(sizes[i]* sizefac)
            D2 = px.Dis(Radiis[i] * Radifac)
            
            pygame.draw.circle(window, (156, 167, 184),
                   [px.coorx(0) , px.coory(0)], D2, 1)
            pygame.draw.circle(window, (0, 255, 0),
                   [px.coorx(P1.X2) , px.coory(P1.Y2)],D1 , 0)
            
    window.blit(text , ( 20 ,windowH - 150))
    pygame.display.update()

    


