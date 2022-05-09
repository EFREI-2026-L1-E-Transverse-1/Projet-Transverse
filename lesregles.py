import pygame
import os

def lesregles():
    pygame.init()


    LARGEUR_ECRAN = 850
    LONGUEUR_ECRAN = 700

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


    bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    #grenade
    grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()


    #Couleurs et fond d'ecran
    BG = pygame.image.load('img/logoefrei.jpg')
    RED = (255, 0, 0)

    def draw_bg():
        screen.blit(BG,(0,0))
        pygame.draw.line(screen, RED, (0, 500), (LARGEUR_ECRAN, 500))



    class Soldier(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.char_type = char_type
            self.speed = speed
            self.ammo = ammo
            self.start_ammo = ammo
            self.tir_cooldown = 0
            self.grenades = grenades
            self.health = 100
            self.max_health = 100
            self.direction = 1
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.flip = False
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()


            animation_types = ['Idle', 'Run', 'Jump', 'Death']
            for animation in animation_types:
                #reset temporary list of images
                temp_list = []
                #count number of files in the folder
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
            self.check_alive()
            #update cooldown
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

            #check collision with floor
            if self.rect.bottom + dy > 500:
                dy = 500 - self.rect.bottom
                self.in_air = False

            #update rectangle position
            self.rect.x += dx
            self.rect.y += dy


        def tir(self):
            if self.tir_cooldown == 0 and self.ammo > 0:
                self.tir_cooldown = 20
                bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
                #reduce ammo
                self.ammo -= 1
            if self.tir_cooldown == 0 and self.ammo > 0:
                self.tir_cooldown = 20
                bullet2 = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group2.add(bullet2)
                #reduce ammo
                self.ammo -= 1

        def update_animation(self):
            #update animation
            ANIMATION_COOLDOWN = 100
            #update image depending on current frame
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if the animation has run out the reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0



        def update_action(self, new_action):
            #check if the new action is different to the previous one
            if new_action != self.action:
                self.action = new_action
                #update the animation settings
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()



        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)


        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):
            #move bullet
            self.rect.x += (self.direction * self.speed)
            #check if bullet has gone off screen
            if self.rect.right < 0 or self.rect.left > LARGEUR_ECRAN:
                self.kill()

            #check collision with characters
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 5
                    self.kill()
            if pygame.sprite.spritecollide(player2, bullet_group2, False):
                if player2.alive:
                    player2.health -= 5
                    self.kill()



    class Grenade(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.timer = 100
            self.vel_y = -14
            self.speed = 7
            self.image = grenade_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):
            self.vel_y += GRAVITE
            dx = self.direction * self.speed
            dy = self.vel_y


            if self.rect.bottom + dy > 500:
                dy = 500 - self.rect.bottom
                self.speed = 0


            if self.rect.left + dx < 0 or self.rect.right + dx > LARGEUR_ECRAN:
                self.direction *= -1
                dx = self.direction * self.speed


            self.rect.x += dx
            self.rect.y += dy



    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()

    bullet_group2 = pygame.sprite.Group()
    grenade_group2 = pygame.sprite.Group()


    player = Soldier('player', 200, 140, 0.4, 5, 50, 50)
    player2 = Soldier('player2', 800, 140, 0.4, 5, 50, 50)



    run = True
    while run:

        clock.tick(FPS)

        draw_bg()

        player.update()
        player.draw()
        player.update_health_bar(screen)    #barre de vie

        player2.update()
        player2.draw()
        player2.update_health_bar(screen)



        bullet_group.update()
        grenade_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)


        bullet_group2.update()
        grenade_group2.update()
        bullet_group2.draw(screen)
        grenade_group2.draw(screen)




        if player.alive:

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


        if player2.alive:

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

                if event.key == pygame.K_UP and player.alive:
                    player.jump = True
                elif event.key == pygame.K_z and player2.alive:
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

    pygame.quit()
