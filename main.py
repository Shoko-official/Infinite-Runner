# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
import time
import random
import sys
from math import sin
from pathlib import Path

def path(relative_path):
    """
    Fonction pour trouver le chemin des ressources, 
    pour que le .exe trouve les images après compilation.
    """
    base_path = Path(getattr(sys, '_MEIPASS', '.'))
    return base_path / relative_path

# Variables Globales
L, H = 1300, 800
FPS = 120
hitbox_activee = True

class Player:
    """
    Classe qui gère le joueur,
    Les méthodes : 
    - __init__ : on initialise les attributs
    - appliquer_gravite : on applique la gravité et on change l'image si on est en l'air
    - saut : explicite je pense
    - animer : gère les animations selon l'action
    - maj : mise à jour de la position et affichage

    Les attributs :
    - p_run : images pour la course
    - p_jump : images pour le saut
    - image_coeur : icône de vie
    - p_run_nb_images : frames course
    - p_jump_nb_images : frames saut
    - image_act : état actuel (course/saut)
    - width, height : dimensions
    - x, y : position
    - force_vert : physique verticale
    - gravite : force de gravité
    - limite_sol : limite de chute
    - frame_index : index d'anim
    - vitesse_anim : vitesse d'anim
    - vitesse_anim_saut : vitesse anim saut
    - hitbox : zone de collision
    - pause : état de pause
    - points_de_vie : vie restante
    """
    def __init__(self):
        self.p_run = pygame.image.load(path("assets/graphics/characters/player/run.png")).convert_alpha()
        self.p_run = pygame.transform.scale(self.p_run, (1024 * 2.5, 128 * 2.5))
        self.p_jump = pygame.image.load(path("assets/graphics/characters/player/jump.png")).convert_alpha()
        self.p_jump = pygame.transform.scale(self.p_jump, (896 * 2.5, 128 * 2.5))
        self.image_coeur = pygame.image.load(path("assets/graphics/items/heart.png")).convert_alpha()        
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
        self.points_de_vie = 3
        
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
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)





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
            self.image = pygame.image.load(path("assets/graphics/environment/mobs/bird/walk.png")).convert_alpha()
            self.nb_frames = 6
            # Redimensionnement par multiplicateur
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            self.y_base = random.randint(100, 350)
            self.y = self.y_base
            self.amplitude = 30
            self.vitesse_haut_bas = 0.04
            self.vitesse = random.uniform(4, 6) # Permets d'avoir une vitesse avec décimale (+ naturel)

        elif nom == "rat":
            self.image = pygame.image.load(path("assets/graphics/environment/mobs/rat/walk.png")).convert_alpha()
            self.nb_frames = 4
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
            # On calcule la hauteur après le scale pour le positionnement
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 35
            self.vitesse = random.uniform(5, 7)

        elif nom == "loup":
            self.image = pygame.image.load(path("assets/graphics/environment/mobs/loup/run.png")).convert_alpha()
            self.nb_frames = 6
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2.2), int(self.image.get_height() * 2.2)))
            h_temp = self.image.get_height()
            self.y = H - 100 - h_temp + 25
            self.vitesse = random.uniform(6, 8)

        elif nom == "ours":
            self.image = pygame.image.load(path("assets/graphics/environment/mobs/ours/run.png")).convert_alpha()
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
            
        rect = (int(self.index) * self.w, 0, self.w, self.h)
        frame_surface = self.image.subsurface(rect)
        self.hitbox = frame_surface.get_bounding_rect()
        self.hitbox.x += self.x
        self.hitbox.y += self.y

        screen.blit(self.image, (self.x, self.y), rect)
        if hitbox_activee:  
            pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)





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
        self.bg_img = pygame.image.load(path("assets/graphics/environment/background/ville/1.png")).convert()
        self.bg_img_2 = pygame.image.load(path("assets/graphics/environment/background/ville/2.png")).convert_alpha()
        self.bg_img_3 = pygame.image.load(path("assets/graphics/environment/background/ville/3.png")).convert_alpha()
        self.bg_img_4 = pygame.image.load(path("assets/graphics/environment/background/ville/4.png")).convert_alpha()
        self.bg_img_5 = pygame.image.load(path("assets/graphics/environment/background/ville/5.png")).convert_alpha()

        self.bg_img = pygame.transform.scale(self.bg_img, (L, H)) 
        self.bg_img_2 = pygame.transform.scale(self.bg_img_2, (L, H))
        self.bg_img_3 = pygame.transform.scale(self.bg_img_3, (L, H)) 
        self.bg_img_4 = pygame.transform.scale(self.bg_img_4, (L, H))   
        self.bg_img_5 = pygame.transform.scale(self.bg_img_5, (L, H))

        self.sol_img = pygame.image.load(path("assets/graphics/environment/props/ground.png")).convert()
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

class Systeme():
    """
    Classe qui regroupe les différentes éléments d'interface : menu, pts vie ect..
    Les méthodes :
    - fenetre_game_over : affiche la fenêtre game over
    - fenetre_lanceur : affiche la fenêtre de lancement
    - fenetre_pause : affiche la fenêtre de pause
    - afficher_interface : affiche les points de vie
    """
    def fenetre_game_over(screen):
        overlay = pygame.Surface((L, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt_titre = pygame.font.SysFont("Arial", 80, bold=True).render("GAME OVER", True, (255, 105, 97))
        txt_msg = pygame.font.SysFont("Arial", 30).render("Oups.. Appuie sur Espace pour recommencer", True, (200, 200, 200))

        screen.blit(txt_titre, (L//2 - txt_titre.get_width()//2, H//2 - 60))
        screen.blit(txt_msg, (L//2 - txt_msg.get_width()//2, H//2 + 20))

    def fenetre_lanceur(screen):
        overlay = pygame.Surface((L, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        txt_titre = pygame.font.SysFont("Arial", 80, bold=True).render("Get What U Need", True, (255, 255, 255))
        txt_msg = pygame.font.SysFont("Arial", 35).render("Appuie sur ESPACE pour commencer", True, (220, 220, 220))

        screen.blit(txt_titre, (L//2 - txt_titre.get_width()//2, H//2 - 60))
        screen.blit(txt_msg, (L//2 - txt_msg.get_width()//2, H//2 + 20))

    def fenetre_pause(screen):
        overlay = pygame.Surface((L, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        txt_titre = pygame.font.SysFont("Arial", 80, bold=True).render("PAUSE", True, (255, 255, 255))
        txt_msg = pygame.font.SysFont("Arial", 30).render("Appuie sur P ou ESC pour reprendre", True, (200, 200, 200))

        screen.blit(txt_titre, (L//2 - txt_titre.get_width()//2, H//2 - 60))
        screen.blit(txt_msg, (L//2 - txt_msg.get_width()//2, H//2 + 20))

    def afficher_interface(screen, player):
        for i in range(player.points_de_vie):
            screen.blit(player.image_coeur, (20 + (i * 60), 20))

def run():
    """
    Fonction d'affichage et appels aux méthode des classes
    Initialisation : 
    - pygame.init() : démarre les modules de pygame
    - clock = créer un object clock, pour gerrer la vitesse et FPS
    - screen = définit la dimension de la fenêtre selon les variables globales L et H
    - player = création de l'objet Player
    - env = création de l'objet Environnement
    - Continuer = variable qui contrôle la boucle du jeu

    Les variables locales :
    - mobs = liste qui contient les mobs
    - spawn_timer_sol = timer pour le spawn des animaux terrestres
    - spawn_timer_ciel = timer pour le spawn des oiseaux
    """
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((L, H))
    pygame.display.set_caption("Get What U Need")

    player = Player()
    env = Environnement()
    Continuer = True
    mobs = []
    spawn_timer_sol = 0
    spawn_timer_ciel = 0
    jeu_en_cours = False
    multiplicateur = 1.0

    # Boucle du Jeu
    while Continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # On regarde si une touhe est pressée, puis si c'est p ou esc, sinon ca écoute la sourie et lag
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not jeu_en_cours:
                        jeu_en_cours = True
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    player.pause = not player.pause

        if player.points_de_vie <= 0:
            Systeme.fenetre_game_over(screen)
            pygame.display.flip()
            
            # On attend un petit input pour restart proprement
            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # On reset les variables de jeu
                            player = Player()
                            env = Environnement()
                            mobs = []
                            spawn_timer_sol = 0
                            spawn_timer_ciel = 0
                            attente = False
            continue

        if jeu_en_cours and not player.pause:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                player.saut()

            if multiplicateur < 2.5:
                multiplicateur += 0.0001
            env.vitesse_sol = 4 * multiplicateur

            env.defilement()
            player.appliquer_gravite()
            player.animer()

            spawn_timer_sol += 1
            if spawn_timer_sol > (FPS * 3.5) / multiplicateur:
                mobs.append(Mob(random.choice(["loup", "ours", "rat"])))
                spawn_timer_sol = 0

            spawn_timer_ciel += 2
            if spawn_timer_ciel > (FPS * 1.5) / multiplicateur:
                nb_oiseaux = random.randint(0, 1)
                for i in range(nb_oiseaux):
                    nouvel_oiseau = Mob("bird")
                    nouvel_oiseau.x += (i * random.randint(150, 300))
                    nouvel_oiseau.y_base += random.randint(-50, 50)
                    mobs.append(nouvel_oiseau)
                spawn_timer_ciel = 0

        # Gestion de l'affichage
        screen.fill((255, 255, 255))
        env.maj(screen)

        if not jeu_en_cours:
            Systeme.fenetre_lanceur(screen)
        else:
            player.maj(screen)
            Systeme.afficher_interface(screen, player)

            # On parcours les mobs actuels
            for m in mobs[:]:
                if not player.pause:
                    m.maj(screen, multiplicateur)
                else:
                    rect = (int(m.index) * m.w, 0, m.w, m.h)
                    screen.blit(m.image, (m.x, m.y), rect)

                if player.hitbox.colliderect(m.hitbox) and not m.touchee:
                    m.touchee = True
                    player.points_de_vie -= 1
                    
                if not player.pause and m.x < -200:
                    mobs.remove(m)

            if player.pause:
                Systeme.fenetre_pause(screen)

        vitesse_act = round(env.vitesse_sol, 2)
        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')} - Speed: {vitesse_act}")
        pygame.display.flip()
        clock.tick(FPS) # On limite les FPS (pas besoin d'aller excessivement vite, on est qu'en 2d)

if __name__ == "__main__":
    print("Lancement de l'application")
    run()
    print("Arrêt de l'application")
