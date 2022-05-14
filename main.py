###############################
#####                     #####
#####  Projet Transverse  #####
#####      Groupe E5      #####
#####                     #####
###############################

######## IMPORTS #########

# début de structure de menu
import pygame
from pygame import mixer
from nouvellepartie import *
from lesregles import lesregles
from credits import credits

# Initialiaser pygame
pygame.init()
mixer.music.load("assets/mielpops.mp3")
pygame.mixer.music.set_volume(0.45)
mixer.music.play(-1)

# Crée la fenêtre
screen = pygame.display.set_mode((1280, 720))

# Fond du menu
background = pygame.image.load("assets/FONDS_V2.PNG")

# Titre et icone
pygame.display.set_caption("Blobs Battle")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

# Instance du sélectioneur visuel
fleche = pygame.image.load("assets/fleche.xcf")
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

            if event.key == pygame.K_UP:

                if choice != 1:
                    choice -= 1
                    default_selection_y -= choice_space_y

            elif event.key == pygame.K_DOWN:

                if choice != 3:
                    choice += 1
                    default_selection_y += choice_space_y

            elif event.key == pygame.K_RETURN:
                if choice == 1:
                    background = lancer()
                elif choice == 2:
                    background = lesregles()
                elif choice == 3:
                    background = credits()

    default_selection_menu(default_selection_x,default_selection_y)
    pygame.display.update()
