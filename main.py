import pygame

def run():
    pygame.init()
    screen = pygame.display.set_mode((1300, 800))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255, 255, 255))
        pygame.display.flip()

if __name__ == "__main__":
    run()