
add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - Add Library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import random
import time
import processing.sound
import turtle
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
LANGUAGE='PL' 
global kosmos, Komandor #przez Komandor, intro rozumiem gracza
kosmos = "kosmos.jpg"
#intro = "Elite Dangerous intro.mp3" 
tlo2 = "bg_robocze2_TWH.png" #screen CMDR KartonowyMakaron The Winged Hussars 
#komputer_pokladowy = "gretting-commanders.mp3"
powi = "bg_robocze4_TWH.png"

#KLASY

class Pauzowanie():
  def pokaz(self):
    strokeWeight(0)
    fill(255,255,0)
    rect(w/2, h/2, w, h)
    myFont = createFont("Candara Bold", 110)
    textFont(myFont)
    fill(0, 0, 0)
    text("Co jest byczq?? Czemu zapauzowałeś?? Wciśnij se <STRZAŁ>, aby wrócić do akcji!", w/4, h/4)
    
    #możnaby użyć do pauzy coś z tą komendą:
    #def pauza():
      #global pause 
      #if pause == True:
        #pause = False
      #else:
        #pause = True
        # i do tego jeszcze onkeypress(pauza, "p")
        # tylko nie wiem jak to wykorzystać dokładnie w naszej grze
    
    
class Sprite():
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
        text("Witaj! Nacisnij start by zacząć." if LANGUAGE=='PL' else 'Welcome! Click start to begin', 80, 100)
        
class Start():
    def pokaz(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(90, 280, 400, 150)
        myFont = createFont("Candara Bold", 45)
        textFont(myFont)
        fill(255)
        text("START!", 90, 265)
        text("Kliknij enter" if LANGUAGE=='PL' else 'Click ENTER', 90, 330)
        
class Restart():
    def pokaz(self):
        fill(255,255,0)
        rect(90, 280, 400, 150)
        myFont = createFont("Candara Bold", 50)
        textFont(myFont)
        fill(225)
        text("RESTART", 50, height/2-10)
        text("Kliknij delete", 50, height/2+50)
        
        
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
        text("Jestes pewny ze chcesz wyjsc?" if LANGUAGE=='PL' else "youre sure you want to leave" ,w/2, h/2)

        
class Statek():
    maksymalnaPredkosc = 6 # maksymalna prędkość statku
    maksymalnePrzyspieszenie = 6 # maksymalne przyspieszenie statku    
    def __init__(self):    
        self.pozycja = PVector(0, 0)
        self.predkosc = PVector(0, 0)
        self.przyspieszenie = PVector(0, 0)
        self.orientacja = 0 # położenie dzioba statku - kąt w radianach
        self.ochloniecie = 0 # 'cooldown' strzelania - każda klatka animacji zmniejsza tę wartość o 1. Następny pocisk można wystrzelić tylko gdy == 0
        self.rozmiar = 8

    def animuj(self):
        if self.przyspieszenie.magSq() == 0:
            self.predkosc.x *= 0.98 # 
            self.predkosc.y *= 0.98 # efekt zwalniania, gdy nie jest trzymany przycisk gazu 
        else:
            self.predkosc.x += self.przyspieszenie.x
            self.predkosc.y += self.przyspieszenie.y
            self.predkosc.limit(self.maksymalnaPredkosc)
            
        self.pozycja.x += self.predkosc.x;
        self.pozycja.y += self.predkosc.y;
        self.ochloniecie -= 1

    def strzel(self):
        if self.ochloniecie > 0:
            return None
        
        # stwórz nowy pocisk z takim kierunkiem, w jakim jest zwrócony statek
        pozycjaPocisku = self.pozycja.copy()        
        predkoscPocisku = PVector.fromAngle(self.orientacja)
        self.ochloniecie = 20
        return Pocisk(pozycjaPocisku, predkoscPocisku)
                            
    def rysuj(self):
        pushMatrix() # zachowaj macierz transformacji
        stroke(255) 
        fill(255)
        translate(self.pozycja.x, self.pozycja.y) # przesuń środek układu współrzędnych na statek                
        rotate(self.orientacja) # wykonaj obrót układu współrzędnych o kąt zgodny z orientacją statku.
                                # Wszystkie operacje na wierzchołkach będą wykonywane w kontekście takiego
                                # układu. Wywołanie popMatrix() na końcu przywraca układ do poprzedniego stanu.                                        
        circle(0, 0, 5 * self.rozmiar)
        line(0, 0, 50, 0)
        popMatrix() # przywróć macierz transformacji
        
    
    def doPrzodu(self): # ustaw predkość do przodu
        PVector.fromAngle(self.orientacja, self.przyspieszenie)
        self.przyspieszenie.limit(self.maksymalnePrzyspieszenie)
        
    def doTylu(self): # ustaw prędkość do tyłu
        PVector.fromAngle(self.orientacja, self.przyspieszenie)
        self.przyspieszenie.x = -self.przyspieszenie.x # 
        self.przyspieszenie.y = -self.przyspieszenie.y # odwróć wektor
        self.przyspieszenie.limit(self.maksymalnePrzyspieszenie)
    
    def naUkos(self): # ustaw prędkość na ukos
        PVector.fromAngle(self.orientacja, self.przyspieszenie)
        self.przyspieszenie.x = self.przyspieszenie.x # tego nie odwaracm
        self.przyspieszenie.y = -self.przyspieszenie.y # odwróć wektor
        self.przyspieszenie.limit(self.maksymalnePrzyspieszenie)
                
    def bezNapedu(self): # wyzeruj przyspieszenie
        self.przyspieszenie.x = 0
        self.przyspieszenie.y = 0

    def obrotLewo(self): # skręć w lewo
        self.orientacja -= 0.18
        if self.orientacja < 0:
            self.orientacja += TWO_PI
    
    def obrotPrawo(self): # skręć w prawo
        self.orientacja += 0.18
        if self.orientacja >= TWO_PI:
            self.orientacja -= TWO_PI
            
class Pocisk():
    maksymalnaPredkosc = 8 # maksymalna prędkość pocisku
    def __init__(self, arg_pozycja, arg_predkosc):
        self.pozycja = arg_pozycja
        self.predkosc = arg_predkosc
        self.predkosc.setMag(Pocisk.maksymalnaPredkosc)
        self.czasZycia = 40 # przez ile ramek ma żyć ten pocisk
        self.rozmiar = 5
    
    def animuj(self):
        self.pozycja.x += self.predkosc.x
        self.pozycja.y += self.predkosc.y

        self.pozycja.x += self.predkosc.x;
        self.pozycja.y += self.predkosc.y;
 
        self.czasZycia -= 1   
    
    def rysuj(self):
        noStroke()
        fill(255, 0, 0)
        circle(self.pozycja.x, self.pozycja.y, 2 * self.rozmiar)
    
    def czyJestMartwy(self):
        return self.czasZycia <= 0
            
class Score():  #przy pomocy tej klasy można utworzyć instancje wyświetlającą na ekranie wynik
    def __init__(self):
        self.points = 0
        self.highestScore = -1
        
    def increase(self):
        self.points += 1
        
    def reset(self):
        self.points = 0
    
    def setHighest(self):
        if self.points > self.highestScore:
            self.highestScore = self.points
            
class Lives():   #na podstawie tej klasy można stworzyć instancje klasy, która pozwoli na wyświetlenie ilości zyć na ekranie
    def __init__(self, amount):
        self.defaultAmount = amount
        self.amount = amount
        
    def lower(self):
        self.amount -= 1
        
    def setDefault(self):
        self.amount = self.defaultAmount
    
    def rysuj(self):
        fill(255, 0, 0)
        myFont = createFont("Candara Bold", 50)
        textFont(myFont)
        text("Liczba zyc: " + str(self.amount), width/2 + 175, 60)

        
class Przeciwnik():
    def __init__(self, pozycja):
        self.pozycja = pozycja
        self.x = 50 + pozycja
        self.y = 50
        self.left = 0
        self.right = 0
        self.down = 0
        self.speed = 10
    def update(self):
        self.right = self.x + 1
        self.x += self.speed
        if not (self.x <= 480):
            self.down = self.y
            self.y += 20
            self.x = 480
            self.speed *= -1
        if not (self.x >= 20):
            self.down = self.y
            self.y += 20
            self.x = 20
            self.speed *= -1

    def zderzenie(self, pociski):
        for i in pociski:
            if i.pozycja == self.pozycja:
                return True
        return False
        
'''class Blocker(sprite.Sprite):
    def __init__(self, size, color, row, column):
        sprite.Sprite.__init__(self)
        self.h = size
        self.= size
        self.color = color
        self.image = Powierzchnia((self.w, self.h)) #trzeba tylko dodać obrazek tych blokerów
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
'''

def change_language():
    global LANGUAGE
    if mousePressed:
        if mouseX>0 and mouseX<250 and mouseY<45 and mouseY>15:
            LANGUAGE='EN' if LANGUAGE=='PL' else 'PL'        
        
def wprowadzImie():
    tlo2 = loadImage("bg_robocze2_TWH.png")
    background(tlo2)
    textSize(32)
    fill(255)
    text("Zmien jezyk" if LANGUAGE=='PL' else 'Change language' ,-w/4-160,-260)
    text('Gora/dol - poruszanie do przodu/do tylu' if LANGUAGE=='PL' else 'Up/down - move forward/backward', - w / 4 + 420, -70)
    text('Lewo/prawo - obrot' if LANGUAGE=='PL' else 'Left/right - rotation', - w / 4 + 420, -30)
    text('Spacja - strzal' if LANGUAGE=='PL' else 'Space - shot', - w / 4 + 420, 10)
    text('Twoje imie dowodco: ' + imie if LANGUAGE=='PL' else 'Your name commandor: ' + imie, - w / 4 + 420, 190)
    powitanie = Powitanie()
    start = Start()
    powitanie.wyswietl()
    start.pokaz() 
        
def koniecGry(lost, lost_count, lives, run):
    background(127)
    #if lives <= 0 or player.health <= 0:
            #lost = True
            #lost_count += 1
    #if lost:
           #if lost_count > 0:
           #    run = False
           #else:
           #    continue
    
def keyReleased():
    global imie
    global statusGry    
    if statusGry == 2:
        graj()
    if statusGry == 3:
        koniecGry()
        
statek = Statek()
pociski = []
kamienie = []    
        
def graj(): # na razie póki nie ma gry
    global statusGry
    background(0)
    restart = Restart()
    restart.pokaz()
    statek.animuj()
    statek.rysuj()      
        
    for pocisk in pociski:
        pocisk.animuj()
        pocisk.rysuj()
 
    if len(pociski) != 0 and pociski[0].czyJestMartwy(): # wystarczy sprawdzić tylko pierwszy pocisk - następne nie mogą być jeszcze martwe
        pociski.pop(0)
            
def keyPressed():
    if statusGry == 2:           
        if keyCode == UP:
            statek.doPrzodu()
        if keyCode == DOWN:
            statek.doTylu()
        if keyCode == LEFT:
            statek.obrotLewo()
        if keyCode == RIGHT:
            statek.obrotPrawo()
        if key == ' ':
            nowyPocisk = statek.strzel()
            if nowyPocisk is not None:
                pociski.append(nowyPocisk)
                
def keyReleased():
    global imie
    global statusGry    
    if statusGry == 2:
        if keyCode == UP or keyCode == DOWN:
            statek.bezNapedu()  
        if key == DELETE:
          statusGry = 1
            
def keyTyped():
    global imie
    global statusGry
    if statusGry == 1:        
        if key == ENTER:
            statusGry = 2   
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
    frameRate(60)
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
    
    #regulacja dzwieku
    if (keyPressed):
      if (key == "P"): 
          komputer_pokladowy.stop()
      if(key == "M"):
         komputer_pokladowy.play()
        
    
    
def draw():
    translate(630, 300) # przsuń środek układu współrzędnych na środek okna
    change_language()
    if statusGry == 1: # wprowadź imię
        wprowadzImie()
    elif statusGry == 2: # graj
        graj()
    elif statusGry == 3: #wyświetl ekran końcowy
        koniecGry()
    
   #Ruch 
def ruch_lewy():
  x = player.xcor()
  x -= playerspeed
  if x < -280: # przykładowa wartość
    x = -280 # przykładowa wartość
  player.setx(x)
  
def ruch_prawy():
  x = player.xcor()
  x += playerspeed
  if x > -280: # przykładowa wartość # przykładowa wartość
    x = 280 # przykładowa wartość
  player.setx(x)
  
    #bind klawiszy + import turtle
'''--------------------------------nie działą, bo brakuje importu turtle
turtle.listen()
turtle.onkey(ruch_lewy, "Left")
turtle.onkey(ruch_prawy, "Right")
'''
    
    
    # może ktoś się odważy wprowadzić działanie ruchu gracza/przeciwników/strzał?
    
