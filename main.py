import pygame
import time

def run():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Get What U Need")
    screen = pygame.display.set_mode((1300, 800))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
        pygame.display.set_caption("Get What U Need - {}".format(time.strftime("%Hh%M")))
        screen.fill((255, 255, 255))
        pygame.display.flip()

        clock.tick(120)

if __name__ == "__main__":
    print("-----------------")
    print("Le jeu est lancé")
    run()
    print("Le jeu est terminé")