## Lancement du jeu

from time import sleep
import pygame
from pygame import mixer
import os

def nouvellepartie():

    pygame.init()
    mixer.music.load("img/megalovania.mp3")
    pygame.mixer.music.set_volume(0.4)
    mixer.music.play(0)
    n = 0
    mort = 0;

    death_sound = mixer.Sound("img/jeanne.mp3")
               

    LARGEUR_ECRAN = 1280
    LONGUEUR_ECRAN = 720

    screen = pygame.display.set_mode((LARGEUR_ECRAN, LONGUEUR_ECRAN))
    pygame.display.set_caption('Blobs Battle!')

    # Le nombre d'image par seconde (fludité)
    clock = pygame.time.Clock()
    FPS = 60

    #Variable de gravité
    GRAVITE = 0.4

    #Variable personnage
    mouvement_gauche = False
    mouvement_droite = False
    mouvement_gauche2 = False
    mouvement_droite2 = False
    tir = False
    tir2 = False
    grenade = False
    grenade_thrown = False
 
    grenade2 = False
    grenade_thrown2 = False

    projectile_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    #grenade
    grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

    #Couleurs et fond d'ecran
    BG = pygame.image.load('img/bg.jpg')
    RED = (255, 0, 0)

    def draw_bg():
        screen.blit(BG,(0,0))
        pygame.draw.line(screen, RED, (0, 500), (LARGEUR_ECRAN, 500))

    class Soldier(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed, ammo, grenades):

            pygame.sprite.Sprite.__init__(self)
            self.en_vie = True
            self.char_type = char_type
            self.tir_cooldown = 0
            self.grenades = grenades
            self.health = 100
            self.max_health = 100
            self.direction = 1
            self.vel_y = 0
            self.start_ammo = ammo
            self.jump = False
            self.in_air = True
            self.flip = False
            self.speed = speed
            self.ammo = ammo
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

            animation_types = ['Immobile', 'Course', 'Saut', 'Mort']

            for animation in animation_types:

                # Renitialiser temporairement la liste des images
                temp_list = []
           
                num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))

                for i in range(num_of_frames):
                    img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)

                self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):

            self.update_animation()
            self.check_en_vie()
            #mettre a jour le delai d'animation

            if self.tir_cooldown > 0:
                self.tir_cooldown -= 1

        def update_health_bar(self, surface):

            #couleur de la barre de vie et de l'arrière plan
            bar_color = (255,0,0)
            bar_under_color = (222,222,222)

            #definition de la barre de vie
            bar_pos = [self.rect.x + 20, self.rect.y - 14, self.health, 6]
            bar_under_pos = [self.rect.x + 20, self.rect.y - 14, self.max_health, 6]
            
            #affichage de la barre de vie
            pygame.draw.rect(surface, bar_under_color, bar_under_pos)
            pygame.draw.rect(surface, bar_color, bar_pos)
            
        def damage(self, amount):
            # dégats reçus
            self.health -= amount

        def move(self, mouvement_gauche, mouvement_droite):
            dx = 0
            dy = 0

            if mouvement_gauche:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if mouvement_droite:
                dx = self.speed
                self.flip = False
                self.direction = 1

            if self.jump == True and self.in_air == False:
                self.vel_y = -11
                self.jump = False
                self.in_air = True

            self.vel_y += GRAVITE
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

            # verification colision avec le sol
            if self.rect.bottom + dy > 500:
                dy = 500 - self.rect.bottom
                self.in_air = False

           
            self.rect.x += dx
            self.rect.y += dy

        def tir(self):

            if self.tir_cooldown == 0 and self.ammo > 0:
                self.tir_cooldown = 15
                projectile = Projectile(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                projectile_group.add(projectile)
           
                self.ammo -= 1

            if self.tir_cooldown == 0 and self.ammo > 0:
                self.tir_cooldown = 40
                projectile2 = Projectile(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                projectile_group2.add(projectile2)
                self.ammo -= 1

        def update_animation(self):

            ANIMATION_COOLDOWN = 100

            self.image = self.animation_list[self.action][self.frame_index]

            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

 
            if self.frame_index >= len(self.animation_list[self.action]):

                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
 
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_en_vie(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.en_vie = False
                self.update_action(3)


        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        def degats(self):
            if pygame.sprite.spritecollide(player, grenade_group2, False):
                if player.en_vie:
                    player.health -= 1
                    grenade_group2.remove()
            if pygame.sprite.spritecollide(player2, grenade_group, False):
                if player2.en_vie:
                    player2.health -= 1
                    grenade_group.remove()

    class Projectile(pygame.sprite.Sprite):

        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = projectile_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):


            self.rect.x += (self.direction * self.speed)

            if self.rect.right < 0 or self.rect.left > LARGEUR_ECRAN:
                self.kill()

            if pygame.sprite.spritecollide(player, projectile_group, False):
                if player.en_vie:
                    player.health -= 5
                    self.kill()

            if pygame.sprite.spritecollide(player2, projectile_group, False):
                if player2.en_vie:
                    player2.health -= 5
                    self.kill()

    class Grenade(pygame.sprite.Sprite):

        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.timer = 100
            self.vel_y = -14
            self.speed = 9
            self.image = grenade_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction
       

        def update(self):
            self.vel_y += GRAVITE
            dx = self.direction * self.speed
            dy = self.vel_y*0.8

            if self.rect.bottom + dy > 500:
                dy = 500 - self.rect.bottom
                self.speed = 0
                self.kill()

            if self.rect.left + dx < 0 or self.rect.right + dx > LARGEUR_ECRAN:
                self.direction *= -1
                dx = self.direction * self.speed

            self.rect.x += dx
            self.rect.y += dy

      
            if pygame.sprite.spritecollide(player, grenade_group2, False):
                if player.en_vie:
                    player.health -= 10
                    self.kill()

            if pygame.sprite.spritecollide(player2, grenade_group, False):
                if player2.en_vie:
                    player2.health -= 10
                    self.kill()

    projectile_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()

    projectile_group2 = pygame.sprite.Group()
    grenade_group2 = pygame.sprite.Group()

    player = Soldier('player', 200, 140, 0.4, 5, 500, 500)
    player2 = Soldier('player2', 600, 140, 0.4, 5, 500, 500)
    re =0
    run = True
    while run:


        clock.tick(FPS)

        draw_bg()

        player.update()
        player.draw()
        player.update_health_bar(screen)    #barre de vie
        player.degats()

        player2.update()
        player2.draw()
        player2.update_health_bar(screen)
        player2.degats()

        projectile_group.update()
        grenade_group.update()
        projectile_group.draw(screen)
        grenade_group.draw(screen)

        projectile_group2.update()
        grenade_group2.update()
        projectile_group2.draw(screen)
        grenade_group2.draw(screen)
        if(n==1):
            death_sound.set_volume(0.9)
            death_sound.play()
            mort = 1
            
        if player.en_vie:

            if tir:
                player.tir()

            elif grenade and grenade_thrown == False and player.grenades > 0:
             
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                    player.rect.top, player.direction)
                grenade_group.add(grenade)

                player.grenades -= 1
                grenade_thrown = True

            if player.in_air:
                player.update_action(2)

            elif mouvement_gauche or mouvement_droite:
                player.update_action(1)
            

            else:
                player.update_action(0)
            player.move(mouvement_gauche, mouvement_droite)
        else:
            n = n + 1
       
            

        if player2.en_vie:

            if tir2:
                player2.tir()

            elif grenade2 and grenade_thrown2 == False and player2.grenades > 0:
                grenade2 = Grenade(player2.rect.centerx + (0.5 * player2.rect.size[0] * player2.direction),\
                    player2.rect.top, player2.direction)
                grenade_group2.add(grenade2)
                player2.grenades -= 1
                grenade_thrown2 = True

            if player2.in_air:
                player2.update_action(2)

            elif mouvement_gauche2 or mouvement_droite2:
                player2.update_action(1)

            else:
                player2.update_action(0)
            
            player2.move(mouvement_gauche2, mouvement_droite2)
        else:
            n = n + 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    mouvement_gauche = True

                elif event.key == pygame.K_RIGHT:
                    mouvement_droite = True

                elif event.key == pygame.K_q:
                    mouvement_gauche2 = True

                elif event.key == pygame.K_d:
                    mouvement_droite2 = True

                if event.key == pygame.K_UP and player.en_vie:
                    player.jump = True

                elif event.key == pygame.K_z and player2.en_vie:
                    player2.jump = True

                elif event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    mouvement_gauche = False

                elif event.key == pygame.K_RIGHT:
                    mouvement_droite = False

                elif event.key == pygame.K_q:
                    mouvement_gauche2 = False

                elif event.key == pygame.K_d:
                    mouvement_droite2 = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    grenade = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    grenade = False
                    grenade_thrown = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    tir = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    tir = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    grenade2 = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    grenade2 = False
                    grenade_thrown2 = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    tir2 = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    tir2 = False
        

        pygame.display.update()
        
        if(mort==1):
            if (re==170):

                BG=nouvellepartie()
                

                

            else:
                re+=1
                police = pygame.font.SysFont("Comic Sans MS" ,80)
                image_texte = police.render ( "GAME OVER", 1 , (255,0,0) )
                screen.blit(image_texte, (370,560))
                pygame.display.flip()
                

            
    
    pygame.quit()
