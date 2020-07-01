add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import random
import time
import processing.sound

#Colors

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (240 ,255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 140, 0)
CHOCOLATE = (123, 63, 0)
PINK = (255, 192, 203)
GREY = (128, 128, 128)

#ZMIENNE

global kosmos, Komandor #przez Komandor, intro rozumiem gracza
kosmos = "kosmos.jpg"
intro = "Elite Dangerous intro.mp3" 
tlo2 = "bg_robocze_TWH.jpg"

#KLASY

class Sprite():
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        
class Tlo():
    def wyswietl(self,img):
        img = loadImage(kosmos)
        image(img, width/2, height/2)
        
class Powitanie():
    def wyswietl(self):
        strokeWeight(0)
        fill(252, 237, 10)
        rect(width/2,height/2-10, width/2, 100)
        textSize(50)
        fill(0, 0, 0)
        text("Hello! Press start to begin.", width/2, height/2)
        
class Start():
    def pokaz(self):
        strokeWeight(5)
        fill(184, 57, 90)
        rect(width/2, height/2+250, width/4, 80)
        textSize(45)
        fill(171, 207, 210)
        text("Start!", width/2, height/2+265)


class Logowanie(): #to na razie nie działa ale będzie :D
    def zaloguj(self, tlo2):
        tlo2 = loadImage(tlo2)
        image(tlo2, width/2, height/2)
        textSize(20)
        text("Witaj w kosmosie, Komandorze!")
    

class Wyjdz():
    def zobacz(self):
        strokeWeight(5)
        fill(255, 192, 203)
        rect(width/2, height/2+120, width/3, 90)
        textSize(40)
        fill(236, 69, 153)

        #text("Are you sure you want to leave?",width/2, height/2) # <---- nakłada się na poczatkowy napis czy chcesz zacząć dlatego wykomentowałam
        #text("Are you sure you want to leave?",width/2, height/2)

        
class Ship(Sprite): #baza obiektu statku
    def __init__(self):
        self.image = IMG['ship']
        self.speed = 6
        self.rect = self.image.get_rect(topleft=(375, 540))
        
    def ruchy(self, toLeft): #ruchy obiektu
        if toLeft:
            self.x = self.x + (Ship.right - Ship.left)
        else:
            self.x = self.x + (Ship.left - Ship.right)
        if self.x > width:
            self.x = 0
    
def setup():
    size(1280, 720)
    frameRate(30)
    imageMode(CENTER)
    textAlign(CENTER)
    rectMode(CENTER)
    myFont = createFont("Book Antiqua", 15)
    textFont(myFont)
    pass
    global tlo
    tlo = Tlo()

    logowanie = Logowanie()
    powitanie = Powitanie()
    start = Start()
    wyjdz = Wyjdz()
    tlo.wyswietl(kosmos)
    powitanie.wyswietl()
    start.pokaz()
    wyjdz.zobacz()
    
    #dzwiek
    intro = SoundFile(this, "Elite Dangerous intro.mp3")
    intro.play()

    
def draw():
    pass

def mouseClicked():
    global x
    x = mouseX
    global y
    y = mouseY
    if x > 480 and x < 800 and y > 570 and y < 650:
        clear()
        tlo.wyswietl(kosmos)
