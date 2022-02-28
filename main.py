###############################
#####                     #####
#####  Projet Transverse  #####
#####      Groupe E5      #####
#####                     #####
###############################

######## IMPORTS #########

# import Screen
# from Object.Menu import Menu

####### MAIN MENU ########

# Menu().Display().main()

# début de structure de menu (martin)
import pygame
from nouvellepartie import nouvellepartie
from lesregles import lesregles
from credits import credits

# Initialiaser pygame
pygame.init()

# Crée la fenêtre
screen = pygame.display.set_mode((800, 600))

# Fond du menu
background = pygame.image.load("assets/menu-alt.jpg")

# Titre et icone
pygame.display.set_caption("Blobs Battle")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

fleche = pygame.image.load("assets/fleche.png")
selection_x = 200
selection_y = 223

limite = 1

def selection_menu(x,y):
    screen.blit(fleche, (x, y))

running = True

while running:
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Si la touche est préssée verifier si c'est à gauche ou à droite
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:


                if limite == 2:
                    limite-=1
                    selection_y = 223


                elif limite == 3:
                    limite-=1
                    selection_y = 308



            if event.key == pygame.K_DOWN:

                if limite == 1:
                    limite+=1
                    selection_y = 308


                elif limite == 2:
                    limite+=1
                    selection_y = 393

            if event.key == pygame.K_RETURN:
                if limite ==1:
                    background = nouvellepartie()
                elif limite==2:
                    background = lesregles()
                elif limite==3:
                    background = credits()



    selection_menu(selection_x,selection_y)
    pygame.display.update()
