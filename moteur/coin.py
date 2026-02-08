# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
from moteur.constants import path, hitbox_activee

class Coin:
    """
    Classe pour les pièces d'or.
    Les méthodes :
    - __init__ : initialisaiton des attributs
    - maj : met à jour la pièce
    
    Les attributs :
    - images : liste des images d'animation
    - x : position horizontale
    - y : position verticale
    - index : index de l'image actuelle
    - vitesse_anim : vitesse d'animation
    - hitbox : hitbox de la pièce
    - collectee : booléen pour savoir si la pièce a été collecté
    """
    images = [] 
    
    def __init__(self, x, y):
        if not Coin.images:
            for i in range(1, 11):
                p = path(f"assets/graphics/items/coin/Gold_{i}.png")
                img = pygame.image.load(str(p)).convert_alpha()
                img = pygame.transform.scale(img, (45, 45))
                Coin.images.append(img)
        
        self.x = x
        self.y = y
        self.index = 0
        self.vitesse_anim = 0.15
        self.hitbox = pygame.Rect(self.x, self.y, 40, 40)
        self.collectee = False

    def maj(self, screen, mult=1.0):
        self.x -= 4 * mult
        self.index += self.vitesse_anim
        if self.index >= len(Coin.images):
            self.index = 0
        
        img = Coin.images[int(self.index)]
        self.hitbox.x = self.x + 2
        self.hitbox.y = self.y + 2
        
        screen.blit(img, (self.x, self.y))
        if hitbox_activee:
            pygame.draw.rect(screen, (255, 255, 0), self.hitbox, 2)
