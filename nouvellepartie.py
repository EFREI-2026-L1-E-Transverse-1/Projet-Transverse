import math
import random
import pygame

from functions import *

def lancer():

    pygame.init()

    NOIR = (18, 18, 18)
    BLANC = (217, 217, 217)
    ROUGE = (252, 91, 122)
    BLEU = (78, 193, 246)
    ORANGE = (252,76,2)
    JAUNE = (254,221,0)
    TURQUOISE = (0,249,182)

    SCREEN = largeur, longueur = 500, 800

    info = pygame.display.Info()
    largeur = info.current_w
    longueur = info.current_h

    if largeur >= longueur:
        fenetre = pygame.display.set_mode(SCREEN)
    else:
        fenetre = pygame.display.set_mode(SCREEN | pygame.FULLSCREEN)

    clock = pygame.time.Clock()
    image_par_seconde = 60

    font = pygame.font.SysFont('comic sans ms', 20)

    origine = (30, 340)
    rayon = 250

    u = 50
    g = 9.8

    class Projectile(pygame.sprite.Sprite):
        def __init__(self, u, theta):
            super(Projectile, self).__init__()

            self.u = u
            self.theta = conversionRadian(abs(theta))
            self.x, self.y = origine
            self.color = ROUGE

            self.ch = 0
            self.dx = 2
            
            self.f = self.recupTrajectoire()
            self.range = self.x + abs(self.recupDistance())

            self.path = []

        def tempsEnLAir(self):
            return round((2 * self.u * math.sin(self.theta)) / g, 2)

        def recupDistance(self):
            range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
            return round(range_, 2)

        def recupMaxlongueur(self):
            h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
            return round(h, 2)

        def recupTrajectoire(self):
            return round(g /  (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

        def recupPositionProjectile(self, x):
            return x * math.tan(self.theta) - self.f * x ** 2

        def update(self):
            if self.x >= self.range:
                self.dx = 0
            self.x += self.dx
            self.ch = self.recupPositionProjectile(self.x - origine[0])

            self.path.append((self.x, self.y-abs(self.ch)))
            self.path = self.path[-50:]

            pygame.draw.circle(fenetre, self.color, self.path[-1], 5)
            pygame.draw.circle(fenetre, BLANC, self.path[-1], 5, 1)
           

    projectile_group = pygame.sprite.Group()

    click = False
    tp = None

    theta = -30
    end = recupPosCirconf(theta, origine)
    arct = conversionRadian(theta)
    arcrect = pygame.Rect(origine[0]-30, origine[1]-30, 60, 60)

    running = True
    while running:
        fenetre.fill(NOIR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_r:
                    projectile_group.empty()
                    tp = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            if event.type == pygame.MOUSEBUTTONUP:
                click = False

                pos = event.pos
                theta = recupAngle(pos, origine)
                if -90 < theta <= 0:
                    projectile = Projectile(u, theta)
                    projectile_group.add(projectile)
                    tp = projectile

            if event.type == pygame.MOUSEMOTION:
                if click:
                    pos = event.pos
                    theta = recupAngle(pos, origine)
                    if -90 < theta <= 0:
                        end = recupPosCirconf(theta, origine)
                        arct = conversionRadian(theta)
        
        pygame.draw.line(fenetre, BLANC, origine, (origine[0] + 2500, origine[1]), 2)
        pygame.draw.line(fenetre, BLEU, origine, end, 2)
        pygame.draw.circle(fenetre, ROUGE, origine, 3)


        projectile_group.update()


        title = font.render("blobs battle test projectile, cliquez pour lancer", True, BLANC)
        soustitre = font.render("orienter la droite bleue ppur changer", True, BLANC)
        thetatext = font.render(f"Angle : {int(abs(theta))}", True, BLANC)
        degreetext = font.render(f"{int(abs(theta))}°", True, JAUNE)
        fenetre.blit(title, (30, 20))
        fenetre.blit(soustitre,(30,70))


        pygame.draw.rect(fenetre, (0,0,0), (0, 0, largeur, longueur), 5)
        clock.tick(image_par_seconde)
        pygame.display.update()
                
    pygame.quit()
