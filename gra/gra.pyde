###### I niech stanie się gra #######

import sys
import random

class Sprite():
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed

#Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (240 ,255, 0)

class Ship(Sprite): #baza obiektu statku
    def __init__(self):
        self.image = IMG['ship']
        self.speed = 6
        self.rect = self.image.get_rect(topleft=(375, 540))
    
def setup():
    pass

def draw():
    pass
