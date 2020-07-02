
add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - Add Library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import random
import time
import processing.sound
add_library('pdf')


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
tlo2 = "bg_robocze2_TWH.png" #screen CMDR KartonowyMakaron The Winged Hussars 
komputer_pokladowy = "gretting-commanders.mp3"
login = "bg_robocze_TWH.jpg"

#KLASY

class Sprite(): # <3
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        
class Tlo():
    def wyswietl(self,img):
        img = loadImage(tlo2) #jest na razie tylko na próbe
        image(img, width/2, height/2)
        
class Powitanie():
    def wyswietl(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(width/2,height/2-10, width/2, 100)
        myFont = createFont("Candara Bold", 50)
        textFont(myFont)
        fill(0, 0, 0)
        text("Hello! Press start to begin.", width/2, height/2)
        
class Start():
    def pokaz(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(width/2, height/2+250, width/4, 80)
        myFont = createFont("Candara Bold", 45)
        textFont(myFont)
        fill(255)
        text("START!", width/2, height/2+265)


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
        #fill(236, 69, 153)

        #text("Are you sure you want to leave?",width/2, height/2) # <---- nakłada się na poczatkowy napis czy chcesz zacząć dlatego wykomentowałam
        #text("Are you sure you want to leave?",width/2, height/2)

        
class Ship(Sprite): #baza obiektu statku, trzeba będzie rozróżnić swój od wrogich
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
            
#class Bullets(sprite.Sprite): #też przyda się myślę :D
 #   def __init__(self, xpoz, ypoz, kierunek, speed, filename, strona):
  #      sprite.Sprite.__init__(self)
   #     self.image = IMAGES[filename]
    #    self.rect = self.image.get_rect(topleft=(xpos, ypos))
    #    self.speed = speed
     #   self.direction = direction
      #  self.side = side
       # self.filename = filename
        
#class Blocker(sprite.Sprite):
 #   def __init__(self, size, color, row, column):
  #      sprite.Sprite.__init__(self)
   #     self.height = size
    #    self.width = size
     #   self.color = color
      #  self.image = Powierzchnia((self.width, self.height)) #trzeba tylko dodać obrazek tych blokerów
       # self.image.fill(self.color)
        #self.rect = self.image.get_rect()
        #self.row = row
        #self.column = column

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
    
def setup():
    size(1280, 720)
    frameRate(30)
    imageMode(CENTER)
    textAlign(CENTER)
    rectMode(CENTER)
    #myFont = createFont("Book Antiqua", 15)
    #textFont(myFont)
    pass
    global tlo, login
    tlo = Tlo()
    login = loadImage("bg_robocze.TWH.jpg")
    print(type(log))
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
    komputer_pokladowy = SoundFile(this, "gretting-commanders.mp3")
    komputer_pokladowy.play()

    
def draw():
    pass
    # może ktoś się odważy wprowadzić ruch gracza/przeciwników/strzał?
    # trzeba rozróżnić sytuacje: menu od gry na jakąś zmienną logiczną


def mouseClicked():
    global x
    x = mouseX
    global y
    y = mouseY
    if x > 480 and x < 800 and y > 570 and y < 650: #trzeba będzie dodać warunek, że gdy w menu
        clear()
        tlo.wyswietl(kosmos)
        text("Welcome to Space Invaders 2.0, Commander. \n The game was created by TCwAK.", 580, 300)
        fill (255,255,255,70)
