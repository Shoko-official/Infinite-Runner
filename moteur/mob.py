# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
import random
from math import sin
from moteur.constants import path, L, H, hitbox_activee

class Mob:
    """
    Classe qui gère les animaux,
    Les méthodes : 
    - __init__ : initialisaiton des attributs, et se base sur le type d'animal pour initialiser les attributs nécessaires
    - maj : met à jour l'animal, fonction sinus pour l'oiseau, calcule la hitbox et la vitesse
    
    Les attributs :
    - nom : le nom de l'animal
    - index : l'index de l'animal, pour boucler l'animation quand on est a la fin du spritesheet
    - compteur_vague : le compteur de vague, utile pour le calcule des vagues/ocillations de l'oiseau
    - x : la position horizontale de l'animal
    - y : la position verticale de l'animal
    - y_base : la position verticale de base de l'animal
    - amplitude : l'amplitude de l'oiseau
    - vitesse_haut_bas : la vitesse de l'oiseau
    - vitesse : la vitesse de l'animal
    - image : spritesheet de l'animal
    - nb_frames : le nombre de frames de l'animal
    - w : la largeur de l'animal, pour les hitbox
    - h : la hauteur de l'animal, idem
    """

    def __init__(self, nom):
        self.nom = nom
        self.index = 0
        self.compteur_vague = 0
        self.x = L + random.randint(100, 600)

        # Configure les params selon l'animal
        if nom == "bird":
            self.image = pygame.image.load(str(path("assets/graphics/environment/mobs/bird/walk.png"))).convert_alpha()
            self.nb_frames = 6
            # Redimensionnement par multiplicateur
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            self.y_base = random.randint(100, 350)
            self.y = self.y_base
            self.amplitude = 30
            self.vitesse_haut_bas = 0.04
            self.vitesse = random.uniform(4, 6) # Permets d'avoir une vitesse avec décimale (+ naturel)

        elif nom == "rat":
            self.image = pygame.image.load(str(path("assets/graphics/environment/mobs/rat/walk.png"))).convert_alpha()
            self.nb_frames = 4
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            # On calcule la hauteur après le scale pour le positionnement
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 35
            self.vitesse = random.uniform(5, 7)

        elif nom == "loup":
            self.image = pygame.image.load(str(path("assets/graphics/environment/mobs/loup/run.png"))).convert_alpha()
            self.nb_frames = 6
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2.2), int(self.image.get_height() * 2.2)))
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 25
            self.vitesse = random.uniform(6, 8)

        elif nom == "ours":
            self.image = pygame.image.load(str(path("assets/graphics/environment/mobs/ours/run.png"))).convert_alpha()
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

    def maj(self, screen, multiplicateur=1.0):
        self.x -= self.vitesse * multiplicateur

        if self.nom == "bird":
            self.compteur_vague += self.vitesse_haut_bas
            self.y = self.y_base + sin(self.compteur_vague) * self.amplitude
        self.index += 0.10
        if self.index >= self.nb_frames:
            self.index = 0
            
        # Découpe et affichage du sprite
        zone = (int(self.index) * self.w, 0, self.w, self.h)
        sprite_m = self.image.subsurface(zone)
        self.hitbox = sprite_m.get_bounding_rect()
        self.hitbox.x += self.x
        self.hitbox.y += self.y

        screen.blit(self.image, (self.x, self.y), zone)
        if hitbox_activee:  
            pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
