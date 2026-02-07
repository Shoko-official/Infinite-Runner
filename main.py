import pygame
import time

# Variables Globales
# Fenetre
L = 1300
H = 800

# Perso
x = L // 2
y = H // 2
force_vert = 0
gravite = 0.2

# Utilitaires
distance = 0
couleur = (153, 255, 255)

# Fond
fond_x = 0
vitesse_fond = 2

def run():
    global fond_x, y, force_vert
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Get What U Need")
    screen = pygame.display.set_mode((L, H))
    
    x = L // 2
    y = H // 2
    force_vert = 0
    gravite = 0.2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        pygame.display.set_caption("Get What U Need - {}".format(time.strftime("%Hh%M")))
        screen.fill((255, 255, 255))

        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE] and y == H - 200: force_vert = -10

        fond_x -= vitesse_fond
        if fond_x < -2 * L:
            fond_x = 0

        pygame.draw.rect(screen, (153, 255, 255), (fond_x, 0, L, H))
        pygame.draw.rect(screen, (204, 255, 255), (fond_x + L, 0, L, H))
        pygame.draw.rect(screen, (153, 255, 255), (fond_x + L * 2, 0, L, H))

        # Sol
        pygame.draw.rect(screen, (100, 100, 100), (0, H - 100, L, 100))

        # Perso
        force_vert += gravite
        y += force_vert

        if y > H - 200:
            y = H - 200
            force_vert = 0
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 100))
        pygame.display.flip()

        clock.tick(120)



if __name__ == "__main__":
    print("-----------------")
    print("Le jeu est lancé")
    run()
    print("Le jeu est terminé")