import pygame
import time

# Variables Globales
L, H = 1300, 800

class Player:
    def __init__(self):
        self.p_run = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
        self.p_run = pygame.transform.scale(self.p_run, (1024 * 2.5, 128 * 2.5))

        self.p_jump = pygame.image.load("assets/graphics/characters/player/jump.png").convert_alpha()
        self.p_jump = pygame.transform.scale(self.p_jump, (896 * 2.5, 128 * 2.5))

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
        
    def appliquer_gravite(self):
        # Physique Perso
        self.force_vert += self.gravite
        self.y += self.force_vert

        if self.y > self.limite_sol:
            self.y = self.limite_sol
            self.force_vert = 0
            self.image_act = self.p_run # Sol = Run
        else :
            self.image_act = self.p_jump # Air = Jump
    
    def saut(self):
        if self.y >= self.limite_sol:
            self.force_vert = -10
            self.frame_index = 0 # Sinon on commence pas au début..

    def animer(self):
        # Animation de Saut
        if self.image_act == self.p_jump:
            if self.force_vert > 0 and self.frame_index >= 4 :
                self.frame_index = 4 # On lock à la frame 4 (chute)
            else :
                self.frame_index += self.vitesse_anim_saut 
                if self.frame_index >= self.p_jump_nb_images:
                    self.frame_index = 0 
        # Animation de Course
        else :
            self.frame_index += self.vitesse_anim 
            if self.frame_index >= self.p_run_nb_images:
                self.frame_index = 0
    
    def maj(self, screen):
        zone_decoupe = (int(self.frame_index) * self.width, 0, self.width, self.height)
        screen.blit(self.image_act, (self.x, self.y), zone_decoupe)

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
        self.vitesse_sol = 2.7 # Je la trouvais agréable

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

    while Continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Continuer = False
                return

        if pygame.key.get_pressed()[pygame.K_SPACE] and player.y >= player.limite_sol:
            player.saut()

        env.defilement()
        player.appliquer_gravite()
        player.animer()

        # Affichage
        screen.fill((255, 255, 255))
        env.maj(screen)
        player.maj(screen)

        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')}")
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    run()
