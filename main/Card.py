import pygame, sys, os
from enum import Enum
from pygame.locals import *


class Suit(Enum):
    pik = "black"
    trefl = "black"
    karo = "red"
    kier = "red"


class Card(pygame.sprite.Sprite):
    def __init__(self, sui, rank):
        self.suit = sui
        self.rank = rank
        dir_path = sys.path[0]
        img_path = os.path.join(dir_path, "..\images\{0}_{1}.png".format(rank.name, sui.name))
        self.image = pygame.image.load(img_path)
        #install PIL package
