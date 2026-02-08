# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
from moteur.constants import path, L, H, hitbox_activee

class Player:
    """
    Classe qui gère le joueur,
    Les méthodes : 
    - __init__ : setup du joueur
    - appliquer_gravite : gestion de la chute
    - saut : hop !
    - animer : change les frames
    - maj : update et redraw
    Les attributs :
    - p_run : frames de course
    - p_jump : frames de saut
    - image_coeur : vie
    - p_run_nb_images : total frames course
    - p_jump_nb_images : total frames saut
    - image_act : celle qu'on affiche
    - width, height : taille du sprite
    - x, y : coordonées actuelles
    - force_vert : v-speed
    - gravite : poids du perso
    - limite_sol : hauteur du sol
    - frame_index : index frame
    - vitesse_anim : speed anim 1
    - vitesse_anim_saut : speed anim 2
    - hitbox : zone de collision
    - pause : toggle pause
    - pointson_de_vie : les coeurs
    """
    def __init__(self):
        self.p_run = pygame.image.load(str(path("assets/graphics/characters/player/run.png"))).convert_alpha()
        self.p_run = pygame.transform.scale(self.p_run, (1024 * 2.5, 128 * 2.5))
        self.p_jump = pygame.image.load(str(path("assets/graphics/characters/player/jump.png"))).convert_alpha()
        self.p_jump = pygame.transform.scale(self.p_jump, (896 * 2.5, 128 * 2.5))
        self.image_coeur = pygame.image.load(str(path("assets/graphics/items/heart.png"))).convert_alpha()        
        self.image_coeur = pygame.transform.scale(self.image_coeur, (50, 50)) 
        self.p_run_nb_images = 8
        self.p_jump_nb_images = 7
        self.image_act = self.p_run
        self.width = 320
        self.height = 320

        self.x, self.y = (L-320) // 2, H // 2
        self.force_vert = 0
        self.gravite = 0.2
        self.limite_sol = H - 75 - 320 # Pas 100 pour plus de 3d
        self.frame_index = 0
        self.vitesse_anim = 0.13
        self.vitesse_anim_saut = 0.05
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pause = False
        self.pointson_de_vie = 3 # On commence avec 3 coeurs
        
        
    def appliquer_gravite(self):
        """
        Calcule simplement la gravité selon la force verticale qui augemente au fur et à mesure 
        pour prendre plus de vitesse et s'arrête au sol
        """
        self.force_vert += self.gravite
        self.y += self.force_vert

        # On arrête la gravitée et remets l'animation de run quand on atteind le sol
        if self.y > self.limite_sol:
            self.y = self.limite_sol
            self.force_vert = 0
            self.image_act = self.p_run
        # Sinon l'animation est le saut
        else :
            self.image_act = self.p_jump
    
    def saut(self):
        """
        Méthode de saut basique, on vérifie d'abord qu'on est au sol, histoire d'empêcher
        les double sauts
        """
        if self.y >= self.limite_sol:
            self.force_vert = -10
            self.frame_index = 0
            return True
        return False

    def animer(self):
        """
        Méthode qui anime le sprite selon son action actuelle, en se basant sur l'attribut image_act
        """
        if self.image_act == self.p_jump:
            if self.force_vert > 0 and self.frame_index >= 4 :
                self.frame_index = 4 # On lock à la frame 4 (chute)
            else :
                self.frame_index += self.vitesse_anim_saut 
                if self.frame_index >= self.p_jump_nb_images:
                    self.frame_index = 0 
        else :
            self.frame_index += self.vitesse_anim 
            if self.frame_index >= self.p_run_nb_images:
                self.frame_index = 0
    
    
    def maj(self, screen):
        """
        Méthode qui mets à jour le sprite du joueur, sa hitbox et affiche celle si, si hibox_active est true
        """
        zone_decoupe = (int(self.frame_index) * self.width, 0, self.width, self.height)
        frame_surface = self.image_act.subsurface(zone_decoupe)

        self.hitbox = frame_surface.get_bounding_rect()
        self.hitbox.x += self.x
        self.hitbox.y += self.y
        screen.blit(self.image_act, (self.x, self.y), zone_decoupe)

        if hitbox_activee:
            # On dessine la hitbox en rouge pour debug
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
