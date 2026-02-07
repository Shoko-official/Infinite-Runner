import pygame
import time

# Variables Globales
L, H = 1300, 800

class Player:
    def __init__(self):
        self.p_img = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
        self.p_img = pygame.transform.scale(self.p_img, (2560, 320))
        self.x, self.y = (L-320) // 2, H // 2
        self.force_vert = 0
        self.gravite = 0.2
        self.limite_sol = H - 75 - 320 # Pas 100 pour plus de 3d
        self.frame_index = 0
        self.vitesse_anim = 0.13
        
    def gravite(self):
        # Physique Perso
        self.force_vert += self.gravite
        self.y += self.force_vert

        if self.y > self.limite_sol:
            self.y = self.limite_sol
            self.force_vert = 0
    
    def saut(self):
        if self.y >= self.limite_sol:
            self.force_vert = 0

    def animer(self, nb_images):
        self.frame_index += self.vitesse_anim
        if self.frame_index >= nb_images:
            self.frame_index = 0
    
    def maj(self, screen):
        zone_decoupe = (int(self.frame_index) * self.width, 0, self.width, self.height)
        screen.blit(self.p_img, (self.x, self.y), zone_decoupe)



x, y = (L-320) // 2, H // 2
force_vert = 0
gravite = 0.2
fond_x = 0
sol_x = 0
vitesse_fond = 2
vitesse_sol = 2.7

def run():
    global fond_x, sol_x, y, force_vert
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((L, H))
    pygame.display.set_caption("Get What U Need")

    # Animation
    frame_index = 0
    vitesse_anim = 0.13

    # Assets
    bg_img = pygame.image.load("assets/graphics/environment/background/ville/1.png").convert()
    bg_img = pygame.transform.scale(bg_img, (L, H))

    sol_img = pygame.image.load("assets/graphics/environment/props/ground.png").convert()
    sol_img = pygame.transform.scale(sol_img, (L // 4, 100))
    
    p_img = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
    p_img = pygame.transform.scale(p_img, (2560, 320))

    limite_sol = H - 75 - 320 # Pas 100 pour plus de 3d

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Logique de mouvement et saut
        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE] and y >= limite_sol:
            force_vert = -10

        # Mouvement du fond
        fond_x -= vitesse_fond
        if fond_x <= -L:
            fond_x = 0

        # Mouvement du sol
        sol_x -= vitesse_sol
        if sol_x <= -(L//4):
            sol_x = 0

        # Affichage
        screen.fill((255, 255, 255))
        screen.blit(bg_img, (fond_x, 0))
        screen.blit(bg_img, (fond_x + L, 0))

        for i in range(6):
            screen.blit(sol_img, (sol_x + (i * L//4), H - 100))
        

        # Animation Perso
        frame_index += vitesse_anim
        if frame_index >= 8:
            frame_index = 0

        zone_decoupe = (int(frame_index) * 320, 0, 320, 320)
        screen.blit(p_img, (x, y), zone_decoupe)

        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')}")
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    run()