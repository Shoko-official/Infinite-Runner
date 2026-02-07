import pygame
import time

# Variables Globales
L, H = 1300, 800

class Player:
    def __init__(self):
        self.p_img = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
        self.p_img = pygame.transform.scale(self.p_img, (2560, 320))
        self.width = 320
        self.height = 320
        self.x, self.y = (L-320) // 2, H // 2
        self.force_vert = 0
        self.gravite = 0.2
        self.limite_sol = H - 75 - 320 # Pas 100 pour plus de 3d
        self.frame_index = 0
        self.vitesse_anim = 0.13
        
    def appliquer_gravite(self):
        # Physique Perso
        self.force_vert += self.gravite
        self.y += self.force_vert

        if self.y > self.limite_sol:
            self.y = self.limite_sol
            self.force_vert = 0
    
    def saut(self):
        self.force_vert = -10

    def animer(self, nb_images):
        self.frame_index += self.vitesse_anim
        if self.frame_index >= nb_images:
            self.frame_index = 0
    
    def maj(self, screen):
        zone_decoupe = (int(self.frame_index) * self.width, 0, self.width, self.height)
        screen.blit(self.p_img, (self.x, self.y), zone_decoupe)

class Environnement:
    def __init__(self):
        self.bg_img = pygame.image.load("assets/graphics/environment/background/ville/1.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (L, H))

        self.sol_img = pygame.image.load("assets/graphics/environment/props/ground.png").convert()
        self.sol_img = pygame.transform.scale(self.sol_img, (L // 4, 100))

        self.fond_x = 0
        self.sol_x = 0
        self.sol_w = L // 4
        self.vitesse_fond = 2
        self.vitesse_sol = 2.7 # Je la trouvais agréable

    def defilement(self):
        self.fond_x -= self.vitesse_fond
        if self.fond_x <= -L:
            self.fond_x = 0

        self.sol_x -= self.vitesse_sol
        if self.sol_x <= -L:
            self.sol_x = 0
    
    def maj(self, screen):
        screen.blit(self.bg_img, (self.fond_x, 0))
        screen.blit(self.bg_img, (self.fond_x + L, 0))

        for i in range(6):
            screen.blit(self.sol_img, (self.sol_x + (i * L//4), H - 100))

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
        player.animer(10)

        # Affichage
        screen.fill((255, 255, 255))
        env.maj(screen)
        player.maj(screen)

        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')}")
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    run()
