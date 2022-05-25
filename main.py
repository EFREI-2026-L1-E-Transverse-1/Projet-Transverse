###############################
#####                     #####
#####  Projet Transverse  #####
#####      Groupe E5      #####
#####                     #####
###############################

######## IMPORTS #########dddddd

# début de structure de menu
import pygame
from pygame import mixer
from nouvellepartie import *

# Initialiaser pygame
pygame.init()
mixer.music.load("img/quiveut.mp3")
pygame.mixer.music.set_volume(0.8)
mixer.music.play(0)

# Crée la fenêtre
screen = pygame.display.set_mode((1280, 720))

# Fond du menu
background = pygame.image.load("img/FONDS_V2.PNG")

# Titre et icone
pygame.display.set_caption("Blobs Battle")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

# Instance du sélectioneur visuel
fleche = pygame.image.load("img/fleche.xcf")
choice = 2
choice_space_y = 128
default_selection_x = 700
default_selection_y = 321

def default_selection_menu(x,y):
    screen.blit(fleche, (x, y))

running = True

while running:
    screen.blit(background,(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

 
            if event.key == pygame.K_RETURN:
                    background = nouvellepartie()

    default_selection_menu(default_selection_x,default_selection_y)
    pygame.display.update()
