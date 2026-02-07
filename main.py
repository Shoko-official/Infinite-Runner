import pygame
import time

# Variables Globales
L, H = 1300, 800
x, y = (L-256) // 2, H // 2
force_vert = 0
gravite = 0.2
fond_x = 0
vitesse_fond = 2

def run():
    global fond_x, y, force_vert
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
    
    p_img = pygame.image.load("assets/graphics/characters/player/run.png").convert_alpha()
    p_img = pygame.transform.scale(p_img, (2560, 320))

    limite_sol = H - 100 - 320

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Logique de mouvement et saut
        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE] and y >= limite_sol:
            force_vert = -10

        # Background
        fond_x -= vitesse_fond
        if fond_x <= -L:
            fond_x = 0

        # Affichage
        screen.fill((255, 255, 255))
        screen.blit(bg_img, (fond_x, 0))
        screen.blit(bg_img, (fond_x + L, 0))
        
        # Sol
        pygame.draw.rect(screen, (100, 100, 100), (0, H - 100, L, 100))

        # Physique Perso
        force_vert += gravite
        y += force_vert

        if y > limite_sol:
            y = limite_sol
            force_vert = 0

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