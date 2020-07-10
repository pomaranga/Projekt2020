
add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - Add Library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import math
import random
import time
import processing.sound
#import turtle
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
global kosmos, Komandor, gwiazda #przez Komandor, intro rozumiem gracza
kosmos = "kosmos.jpg"
#intro = "Elite Dangerous intro.mp3" 
tlo2 = "bg_robocze2_TWH.png" #screen CMDR KartonowyMakaron The Winged Hussars 
#komputer_pokladowy = "gretting-commanders.mp3"
powi = "bg_robocze4_TWH.png"


#KLASY

#class Przeciwnik(turtle.Turtle):
#    enemy_speed = 2

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
        
class Start():
    iloscZyc = 0
       
    def pokaz(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(90, 280, 400, 150)
        myFont = createFont("Candara Bold", 45)
        textFont(myFont)
        fill(255)
        text("test", 90, 265)
        text("Kliknij enter" if LANGUAGE=='PL' else 'Click ENTER', 90, 330)
       
    def ustawPoziomTrudnosci(self, poziom):
        if poziom == 'latwy':
            print("Ustawiono poziom łatwy")
            self.__iloscZyc = 6
        elif poziom == 'trudny':
            print("Ustawiono poziom trudny")
            self.__iloscZyc = 3
        else:
            print("Ustawiono poziom łatwy")
            self.__iloscZyc = 6
           
    def czytajPoziomTrudnosci(self):
        return self.__iloscZyc
        
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
        
class Gwiazdy():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def rusz(self):
        fill(255, 255, 255)
        square(self.x, self.y, 5)
        self.y = self.y + self.speed;
        if self.y > height:
            self.y = 0
            self.x = random.randint(0, 1366)
            
gwiazda = Gwiazdy(50, 100, 2)

        
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
#class WybuchStatka(sprite.Sprite):
   #def __init__(self, ship, ):
       #super(WybuchStatka, self).__init__(statek)
       #self.image = image['ship']
       #self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
       #self.timer = time.get_ticks()

   #def update(self, current_time, args):
       #passed = current_time - self.timer
       #if 300 < passed <= 600:
           #game.screen.blit(self.image, self.rect)
       #elif 900 < passed:
           #self.kill()
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
            self.highestScore = self.point
            
    def killpoints(self):
         przeciwnik = 1 #poziom przeciwnika zabitego lub jego liczba HP
         poziom = -1 #Punkty za poziom planszy są naliczane co 5.
         sco = 1 #liczba punktów za normanego przeciwnika
         ostatni = False 
         premia = 20 #premia za przejście poziomu
   
         if(poziom == -1):
            score = sco*przeciwnik
            self.points += score 
         else:
            score = (poziom/5)+sco*przeciwnik
            self.points += score
       
         if (ostatni == True):
            if (poziom == 0):
                poziom = 1
                score = premia*poziom
                self.points += score
            
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
            
    def multiply():
        global wrogowie
        liczba_wrogow = 5 #przykładowe wartości
        wrogowie = []
        pozycja = 0
        for i in range(liczba_wrogow):
            b = Wrog(pozycja)
            wrogowie.append(b)
            pozycja+=50
        
        for wrog in wrogowie:
            pass
   

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
#Narysuj granicę
def draw_frame():
    for i in range(2):
        frame_pen.forward(1200)
        frame_pen.left(90)
        frame_pen.forward(800)
        frame_pen.left(90)

global stan_pocisku
stan_pocisku = 'ready'
def kula_ognia():
    if stan_pocisku == "ready":
        stan_pocisku = "fire"
#umieszcza kulę tuż nad graczem
        x = player.xcor()
        pocisk.setposition(x)
        pocisk.showturtle()

#Sprawdź kolizję między graczem a wrogiem oraz pociskami i wrogiem.

def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False

#przesuń kulę
if stan_pocisku == "fire":
        y = pocisk.ycor()
        y += pocisk_predkosc
        pocisk.sety(y)
                        
#Sprawdź, czy kula osiągnęła szczyt ramki
'''if pocisk.ycor() > 370:
        pocisk.hideturtle()
        stan_pocisku = "ready"
'''                         

HELP = 'NH'
    
def buttonsMenu():
    global statusGry
    global LANGUAGE
    global HELP
   
    if mousePressed:
        if mouseX>60 and mouseX<460 and mouseY>275 and mouseY<324:
            statusGry = 2
        if mouseX>60 and mouseX<460 and mouseY>375 and mouseY<424:
            LANGUAGE='EN' if LANGUAGE=='PL' else 'PL'
        if mouseX>60 and mouseX<460 and mouseY>425 and mouseY<475:
            HELP='YH' if HELP=='NH' else 'NH'
        if mouseX>60 and mouseX<460 and mouseY>565 and mouseY<615:
            exit()
                                  
class Help():
    def pokaz(self):
        stroke(255)
        fill(49, 51, 50, 160)
        rect(280, 90, 800, 600)
        fill(255)
        text('Pomoc' if LANGUAGE=='PL' else 'Help', 270, -170)
        text('Gora/dol - poruszanie do przodu/do tylu' if LANGUAGE=='PL' else 'Up/down - move forward/backward', 270, -70)
        text('Lewo/prawo - obrot' if LANGUAGE=='PL' else 'Left/right - rotation', 270 , -30)
        text('Spacja - strzal' if LANGUAGE=='PL' else 'Space - shot', 270, 10)
        text('P - ...' if LANGUAGE=='PL' else 'P - ...', 270 , 50)
        text('M - ...' if LANGUAGE=='PL' else 'M - ...', 270, 90)

class Error():
    def show(self):
        strokeWeight(7)
        fill(255,0,0)
        rect(55, 65, width/2, height/6)
        fill(0, 0, 0)
        textSize(25)
        text("Error! The game can't find essential files.", 65, 70)
        text("Press 'e' key to exit.", 50, 300)   
        
error = Error()                            
                                                                                
def mainMenu():
    global HELP
    global BSCORE
    try:
        tlo2 = loadImage("bg_robocze2_TWH.png")
        background(tlo2)
        stroke(255)
        fill(49, 51, 50, 160)
        rect(-370, 84, 400, 766)
        fill(255)
        textSize(70)
        text("Super Gra",-370,-160)
        textSize(15)
        text("Ver. 2.0.7.7",-380, 455)
        textSize(32)
        text('Twoje imie dowodco: ' if LANGUAGE=='PL' else 'Your name commandor: ', -365, 240)
        text(imie, -380, 280)
        text("Rozpocznij gre" if LANGUAGE=='PL' else 'Start the game' ,-380, 10)
        text("Zmien jezyk" if LANGUAGE=='PL' else 'Change language' ,-380, 110)
        text("Pomoc" if LANGUAGE=='PL' else 'Help' ,-380, 160)
        text("Wyjdz" if LANGUAGE=='PL' else 'Quit' ,-380, 400)
        start = Start()
        start.ustawPoziomTrudnosci("trudny")
        start.pokaz() 
        if HELP == 'YH':
            help = Help()
            help.pokaz()
    except:
        error.show()
        if keyPressed and key == "e" or key == "E":
            exit()
        
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
    gwiazda.rusz()      
        
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
    if statusGry == 1: # wprowadź imię
        buttonsMenu()
        mainMenu()
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
'''
turtle.listen()
turtle.onkey(ruch_lewy, "Left")
turtle.onkey(ruch_prawy, "Right")
'''

def _collision_found(self, Pocisk, Przeciwnik):
    if Pocisk.x + Pocisk.width < Przeciwnik.x:
        return False
    elif Pocisk.x + Pocisk.width < Pocisk.x:
        return False
    elif Pocisk.y + 1 < Przeciwnik.y:
        return False
    elif Przeciwnik.y + 8 < Pocisk.y:
        return False
    
    return True
    
    # może ktoś się odważy wprowadzić działanie ruchu gracza/przeciwników/strzał?
    
