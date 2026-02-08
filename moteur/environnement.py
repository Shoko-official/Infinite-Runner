# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
from moteur.constants import path, L, H

class Environnement:
    """
    Classe qui gère l'environnement, 
    Les méthodes :
    - __init__ : initialisaiton des attributs
    - defilement : défilement inégal des plans selon la vitesse de chacun
    - maj : met à jour l'environnement
    
    Les attributs :
    - bg_img : ciel
    - bg_img_2 : plan-loin
    - bg_img_3 : plan-éloigné
    - bg_img_4 : plan-proche
    - bg_img_5 : premier-plan
    - sol_img : sol
    - vitesse : vitesse de défilement des plans, effet 3d
    - fond_x : position horizontale des plans, sous forme de liste
    - sol_x : position horizontale du sol
    - sol_w : largeur du sol
    - vitesse_sol : vitesse de défilement du sol
    """
    def __init__(self):
        self.bg_img = pygame.image.load(str(path("assets/graphics/environment/background/ville/1.png"))).convert()
        self.bg_img_2 = pygame.image.load(str(path("assets/graphics/environment/background/ville/2.png"))).convert_alpha()
        self.bg_img_3 = pygame.image.load(str(path("assets/graphics/environment/background/ville/3.png"))).convert_alpha()
        self.bg_img_4 = pygame.image.load(str(path("assets/graphics/environment/background/ville/4.png"))).convert_alpha()
        self.bg_img_5 = pygame.image.load(str(path("assets/graphics/environment/background/ville/5.png"))).convert_alpha()

        self.bg_img = pygame.transform.scale(self.bg_img, (L, H)) 
        self.bg_img_2 = pygame.transform.scale(self.bg_img_2, (L, H))
        self.bg_img_3 = pygame.transform.scale(self.bg_img_3, (L, H)) 
        self.bg_img_4 = pygame.transform.scale(self.bg_img_4, (L, H))   
        self.bg_img_5 = pygame.transform.scale(self.bg_img_5, (L, H))

        self.sol_img = pygame.image.load(str(path("assets/graphics/environment/props/ground.png"))).convert()
        self.sol_img = pygame.transform.scale(self.sol_img, (L // 4, 100))

        self.vitesse = [0.2, 0.2, 1.2, 1.8, 2.2]

        self.fond_x = [0, 0, 0, 0, 0]
        self.sol_x = 0
        self.sol_w = L // 4
        self.vitesse_sol = 4

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
