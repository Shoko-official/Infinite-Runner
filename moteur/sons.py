# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
from moteur.constants import path

class Sons:
    """
    Classe qui regroupe et gère les sons du jeu
    Les méthodes :
    - __init__ : initialise les sons
    - lancer_musique : lance la musique
    """
    def __init__(self):
        # On définit le chemin une fois pour toutes pour les effets
        base_sfx = "assets/audio/sfx/"
        
        self.son_jump = pygame.mixer.Sound(str(path(base_sfx + "jump.wav")))   
        self.son_hit  = pygame.mixer.Sound(str(path(base_sfx + "hurt.wav")))
        self.son_coin = pygame.mixer.Sound(str(path(base_sfx + "coin.wav"))) 
        self.son_over = pygame.mixer.Sound(str(path(base_sfx + "game-over.wav")))

        # J'ai équilibré les volumes selon l'importance
        self.son_jump.set_volume(0.5) 
        self.son_hit.set_volume(0.8)
        self.son_coin.set_volume(0.5)   
        self.son_over.set_volume(0.8)

    def lancer_musique(self, track="background_music.wav", volume=0.2):
        # lance en boucle infinie
        p = str(path("assets/audio/music/" + track))
        pygame.mixer.music.load(p)
        pygame.mixer.music.set_volume(volume) 
        pygame.mixer.music.play(-1)
