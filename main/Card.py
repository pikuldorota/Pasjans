import pygame
from enum import Enum
from pygame.locals import *


class Suit(Enum):
    pik = "black"
    trefl = "black1"
    karo = "red"
    kier = "red1"


class Card(pygame.sprite):
    def __init__(self, sui, rank):
        self.suit = sui
        self.rank = rank
        self.front = pygame.image.load( "..\images\{0}_{1}.png".format(rank.name, sui.name))
        self.x = 20
        self.y = 20
