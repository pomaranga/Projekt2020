
add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - Add Library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import random
import time
import processing.sound
w = 1366 
h = 768
statusGry = 1 # 1 - wprowadź imię
              # 2 - graj
              # 3 - koniec gry 
imie = ''
punkty = 0

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

global kosmos, Komandor, ekran #przez Komandor, intro rozumiem gracza
kosmos = "kosmos.jpg"
intro = "Elite Dangerous intro.mp3" 
tlo2 = "bg_robocze2_TWH.png" #screen CMDR KartonowyMakaron The Winged Hussars 
komputer_pokladowy = "gretting-commanders.mp3"
tlo = "bg_robocze3_TWH.jpg"

#KLASY

class Sprite(): # <3
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        
class Powitanie():
    def wyswietl(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(80, 90, 600, 100)
        myFont = createFont("Candara Bold", 50)
        textFont(myFont)
        fill(0, 0, 0)
        text("Hello! Press start to begin.", 80, 100)
        
class Start():
    def pokaz(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(90, 280, 400, 150)
        myFont = createFont("Candara Bold", 45)
        textFont(myFont)
        fill(255)
        text("START!", 90, 265)
        text("Kliknij enter", 90, 330)

class Zamknij():
    def pokaz(self):
        fill(255)
        myFont = createFont("Candara Bold", 25)
        text("ESC", 690, 450)
        
    
class Wyjdz():
    def zobacz(self):
        strokeWeight(5)
        fill(255, 192, 203)
        rect(w/2, h/2-15, w/2, 90)
        textSize(40)
        fill(236, 69, 153)
        text("Are you sure you want to leave?",w/2, h/2)

        
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
        if self.x > w:
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
        
def wprowadzImie():
    tlo2 = loadImage("bg_robocze2_TWH.png")
    background(tlo2)
    textSize(32)
    fill(255)
    text('Your Name Commander: ' + imie, - w / 4 + 420, 190)
    powitanie = Powitanie()
    start = Start()
    powitanie.wyswietl()
    start.pokaz() 
        
def koniecGry():
    background(127)
    textSize(32)
    fill(255)
    text(imie + 'zdobyles/as ' + str(punkty) + ' punktow', - w / 2 + 30, 0)
    
def keyReleased():
    global imie
    global statusGry    
    if statusGry == 2:
        graj()
    if statusGry == 3:
        koniecGry()
        
        
def graj(): #na razie puki nie ma gry
    clear()
    global statusGry
    tlo2 = loadImage("bg_robocze2_TWH.png")
    background(tlo2)
    textSize(40)
    text("Welcome to Space Invaders 2.0, Commander. \n The game was created by TCwAK.", 80, 80)
    fill (255,255,255)
    zamknij = Zamknij()
    zamknij.pokaz()
            
def keyTyped():
    global imie
    global statusGry
    if statusGry == 1:        
        if key == ENTER:
            statusGry = 2   
        if key == ESC:
            statusGry = 3
        if key == BACKSPACE:
            if len(imie) != 0:
                imie = imie[:-1] # usuń ostatni znak
                
        else:
            imie = imie + key          
def setup():
    size(w, h)
    frameRate(30)
    imageMode(CENTER)
    textAlign(CENTER)
    rectMode(CENTER)
    #myFont = createFont("Book Antiqua", 15)
    #textFont(myFont)
    pass
    global tlo
    tlo = loadImage
    print(type(log))
    
    #dzwiek

    intro = SoundFile(this, "Elite Dangerous intro.mp3")
    intro.play()
    komputer_pokladowy = SoundFile(this, "gretting-commanders.mp3")
    komputer_pokladowy.play()

    
def draw():
    translate(630, 300) # przsuń środek układu współrzędnych na środek okna
    if statusGry == 1: # wprowadź imię
        wprowadzImie()
    elif statusGry == 2: # graj
        graj()
    elif statusGry == 3: #wyświetl ekran końcowy
        koniecGry()
    
