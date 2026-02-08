import pygame
import time
import random
from math import sin

# Variables Globales
L, H = 1300, 800
FPS = 120
hitbox_activee = False

class Player:
    def __init__(self):
        self.p_run = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
        self.p_run = pygame.transform.scale(self.p_run, (1024 * 2.5, 128 * 2.5))
        self.p_jump = pygame.image.load("assets/graphics/characters/player/jump.png").convert_alpha()
        self.p_jump = pygame.transform.scale(self.p_jump, (896 * 2.5, 128 * 2.5))
        self.image_coeur = pygame.image.load("assets/graphics/items/heart.png").convert_alpha()        
        self.image_coeur = pygame.transform.scale(self.image_coeur, (50, 50)) 
        self.p_run_nb_images = 8
        self.p_jump_nb_images = 7
        self.image_act = self.p_run
        self.width = 320
        self.height = 320

        self.x, self.y = (L-320) // 2, H // 2
        self.force_vert = 0
        self.gravite = 0.2
        self.limite_sol = H - 75 - 320 # Pas 100 pour plus de 3d
        self.frame_index = 0
        self.vitesse_anim = 0.13
        self.vitesse_anim_saut = 0.05
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pause = False
        self.points_de_vie = 3
        
    def appliquer_gravite(self):
        # On applique la gravité et on change l'image si on est en l'air
        self.force_vert += self.gravite
        self.y += self.force_vert

        if self.y > self.limite_sol:
            self.y = self.limite_sol
            self.force_vert = 0
            self.image_act = self.p_run
        else :
            self.image_act = self.p_jump
    
    def saut(self):
        # Un petit saut sympatoch
        if self.y >= self.limite_sol:
            self.force_vert = -10
            self.frame_index = 0

    def animer(self):
        # Gestion des animations (run vs jump)
        if self.image_act == self.p_jump:
            if self.force_vert > 0 and self.frame_index >= 4 :
                self.frame_index = 4 # On lock à la frame 4 (chute)
            else :
                self.frame_index += self.vitesse_anim_saut 
                if self.frame_index >= self.p_jump_nb_images:
                    self.frame_index = 0 
        else :
            self.frame_index += self.vitesse_anim 
            if self.frame_index >= self.p_run_nb_images:
                self.frame_index = 0
    
    
    def maj(self, screen):
        # Mise à jour de la position et affichage
        zone_decoupe = (int(self.frame_index) * self.width, 0, self.width, self.height)
        frame_surface = self.image_act.subsurface(zone_decoupe)

        # On calcule la hitbox réelle source https://www.pygame.org/docs/ref/surface.html
        self.hitbox = frame_surface.get_bounding_rect()
        self.hitbox.x += self.x
        self.hitbox.y += self.y
        screen.blit(self.image_act, (self.x, self.y), zone_decoupe)

        if hitbox_activee:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def vie_restante(self, screen):
        # Affichage des points de vie (les petits coeurs)
        for i in range(self.points_de_vie):
            screen.blit(self.image_coeur, (20 + (i * 60), 20))

    def fenetre_pause(self, screen):
        # Le menu de pause basique
        surface_pause = pygame.Surface((L, H), pygame.SRCALPHA)
        surface_pause.fill((0, 0, 0, 150))
        screen.blit(surface_pause, (0, 0))

        txt_p = pygame.font.SysFont("Arial", 80).render("PAUSE", True, (255, 255, 255))
        txt_r = pygame.font.SysFont("Arial", 30).render("Presse P ou ECHAP pour recommencer", True, (200, 200, 200))

        screen.blit(txt_p, (L//2 - txt_p.get_width()//2, H//2 - 50))
        screen.blit(txt_r, (L//2 - txt_r.get_width()//2, H//2 + 50))

    def fenetre_game_over(self, screen):
        # L'écran quand on a perdu
        surface_game_over = pygame.Surface((L, H), pygame.SRCALPHA)
        surface_game_over.fill((0, 0, 0, 150))
        screen.blit(surface_game_over, (0, 0))

        txt_p = pygame.font.SysFont("Arial", 80).render("GAME OVER", True, (255, 255, 255))
        txt_r = pygame.font.SysFont("Arial", 30).render("Une prochaine fois peut-être", True, (200, 200, 200))

        screen.blit(txt_p, (L//2 - txt_p.get_width()//2, H//2 - 50))
        screen.blit(txt_r, (L//2 - txt_r.get_width()//2, H//2 + 50))

class Mob:
    def __init__(self, nom):
        self.nom = nom
        self.index = 0
        self.compteur_vague = 0
        self.x = L + random.randint(100, 600)

        # Configuration manuelle
        if nom == "bird":
            self.image = pygame.image.load("assets/graphics/environment/mobs/bird/walk.png").convert_alpha()
            self.nb_frames = 6
            # Redimensionnement par multiplicateur
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            self.y_base = random.randint(100, 350)
            self.y = self.y_base
            self.amplitude = 30
            self.vitesse_haut_bas = 0.04
            self.vitesse = random.uniform(4, 6)

        elif nom == "rat":
            self.image = pygame.image.load("assets/graphics/environment/mobs/rat/walk.png").convert_alpha()
            self.nb_frames = 4
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            # On calcule la hauteur après le scale pour le positionnement
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 35
            self.vitesse = random.uniform(5, 7)

        elif nom == "loup":
            self.image = pygame.image.load("assets/graphics/environment/mobs/loup/run.png").convert_alpha()
            self.nb_frames = 6
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2.2), int(self.image.get_height() * 2.2)))
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 25
            self.vitesse = random.uniform(6, 8)

        elif nom == "ours":
            self.image = pygame.image.load("assets/graphics/environment/mobs/ours/run.png").convert_alpha()
            self.nb_frames = 6
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 20
            self.vitesse = random.uniform(4, 5)

        # Dimensions pour la découpe et hitbox
        self.w = self.image.get_width() // self.nb_frames
        self.h = self.image.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.w, self.h)
        self.touchee = False

    def maj(self, screen):
        self.x -= self.vitesse

        if self.nom == "bird":
            self.compteur_vague += self.vitesse_haut_bas
            self.y = self.y_base + sin(self.compteur_vague) * self.amplitude

        self.index += 0.15
        if self.index >= self.nb_frames:
            self.index = 0
            
        rect = (int(self.index) * self.w, 0, self.w, self.h)
        frame_surface = self.image.subsurface(rect)

        # Hitbox dynamique basée sur les pixels visibles
        self.hitbox = frame_surface.get_bounding_rect()
        self.hitbox.x += self.x
        self.hitbox.y += self.y

        screen.blit(self.image, (self.x, self.y), rect)
        if hitbox_activee:  
            pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

class Environnement:
    def __init__(self):
        self.bg_img = pygame.image.load("assets/graphics/environment/background/ville/1.png").convert()
        self.bg_img_2 = pygame.image.load("assets/graphics/environment/background/ville/2.png").convert_alpha()
        self.bg_img_3 = pygame.image.load("assets/graphics/environment/background/ville/3.png").convert_alpha()
        self.bg_img_4 = pygame.image.load("assets/graphics/environment/background/ville/4.png").convert_alpha()
        self.bg_img_5 = pygame.image.load("assets/graphics/environment/background/ville/5.png").convert_alpha()

        self.bg_img = pygame.transform.scale(self.bg_img, (L, H)) 
        self.bg_img_2 = pygame.transform.scale(self.bg_img_2, (L, H))
        self.bg_img_3 = pygame.transform.scale(self.bg_img_3, (L, H)) 
        self.bg_img_4 = pygame.transform.scale(self.bg_img_4, (L, H))   
        self.bg_img_5 = pygame.transform.scale(self.bg_img_5, (L, H))

        self.sol_img = pygame.image.load("assets/graphics/environment/props/ground.png").convert()
        self.sol_img = pygame.transform.scale(self.sol_img, (L // 4, 100))

        self.vitesse = [0.2, 0.2, 1.2, 1.8, 2.2]

        self.fond_x = [0, 0, 0, 0, 0] # liste car les positions sont différentes
        self.sol_x = 0
        self.sol_w = L // 4
        self.vitesse_sol = 4 # Je la trouvais agréable

    def defilement(self):
        for i in range(5):
            self.fond_x[i] -= self.vitesse[i]
            if self.fond_x[i] <= -L:
                self.fond_x[i] = 0

        self.sol_x -= self.vitesse_sol
        if self.sol_x <= -self.sol_w:
            self.sol_x = 0
    
    def maj(self, screen):
        screen.blit(self.bg_img, (self.fond_x[0], 0))
        screen.blit(self.bg_img, (self.fond_x[0] + L, 0))
        
        screen.blit(self.bg_img_2, (self.fond_x[1], -100))
        screen.blit(self.bg_img_2, (self.fond_x[1] + L, -100))
        
        screen.blit(self.bg_img_3, (self.fond_x[2], -100))
        screen.blit(self.bg_img_3, (self.fond_x[2] + L, -100))
        
        screen.blit(self.bg_img_4, (self.fond_x[3], -100))
        screen.blit(self.bg_img_4, (self.fond_x[3] + L, -100))
        
        screen.blit(self.bg_img_5, (self.fond_x[4], -100))
        screen.blit(self.bg_img_5, (self.fond_x[4] + L, -100))

        for i in range(6):
            screen.blit(self.sol_img, (self.sol_x + (i * self.sol_w), H - 100))

def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((L, H))
    pygame.display.set_caption("Get What U Need")

    player = Player()
    env = Environnement()
    Continuer = True
    mobs = []
    spawn_timer_sol = 0
    spawn_timer_ciel = 0

    while Continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Continuer = False
                return
            
            if event.type == pygame.KEYDOWN: # Sinon la sourie est vérifié en continu = lag inutile
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    player.pause = not player.pause

        if player.points_de_vie <= 0:
            print("GAME OVER")
            player.fenetre_game_over(screen)
            pygame.display.flip()
            pygame.time.delay(5000)
            Continuer = False
            return

        if not player.pause:
            if pygame.key.get_pressed()[pygame.K_SPACE] and player.y >= player.limite_sol:
                player.saut()

            env.defilement()
            player.appliquer_gravite()
            player.animer()

            spawn_timer_sol += 1
            if spawn_timer_sol > FPS * 3.5:
                mobs.append(Mob(random.choice(["loup", "ours", "rat"])))
                spawn_timer_sol = 0

            spawn_timer_ciel += 2
            if spawn_timer_ciel > FPS * 1.5:
                nb_oiseaux = random.randint(0, 1)
                for i in range(nb_oiseaux):
                    nouvel_oiseau = Mob("bird")
                    nouvel_oiseau.x += (i * random.randint(150, 300))
                    nouvel_oiseau.y_base += random.randint(-50, 50)
                    mobs.append(nouvel_oiseau)
                spawn_timer_ciel = 0

        screen.fill((255, 255, 255))
        env.maj(screen)
        player.maj(screen)
        player.vie_restante(screen)

        for m in mobs[:]:
            if not player.pause:
                m.maj(screen)
            else:
                rect = (int(m.index) * m.w, 0, m.w, m.h)
                screen.blit(m.image, (m.x, m.y), rect)

            if player.hitbox.colliderect(m.hitbox) and not m.touchee:
                print("Collision détectée")
                m.touchee = True
                player.points_de_vie -= 1
                
            if not player.pause and m.x < -200:
                mobs.remove(m)

        if player.pause:
            player.fenetre_pause(screen)

        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')}")
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run()
