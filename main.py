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

from moteur.constants import L, H, FPS
from moteur.player import Player
from moteur.mob import Mob
from moteur.coin import Coin
from moteur.environnement import Environnement
from moteur.systeme import Systeme
from moteur.sons import Sons

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
    son = Sons()
    son.lancer_musique()
    
    Continuer = True
    # Init des listes et timers
    mobs = []
    coins = []
    
    spawn_timer_sol = 0
    spawn_timer_ciel = 0
    spawn_timer_coin = 0
    
    jeu_en_cours = False
    multiplicateur = 1.0 # La difficulté qui grimpe tout doucement
    score = 0
    

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
                    player.pause = not player.pause # Toggle pause
    

        if player.pointson_de_vie <= 0:
            son.son_over.play()
            pygame.mixer.music.stop()
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
                            # On créer les objets
                            player = Player()
                            env = Environnement()
                            
                            # Réinitialisation des var
                            son.lancer_musique()
                            mobs = []
                            coins = []
                            score = 0
                            spawn_timer_sol = 0
                            spawn_timer_ciel = 0
                            spawn_timer_coin = 0
                            multiplicateur = 1.0
                            attente = False
            continue

        if jeu_en_cours and not player.pause:
            if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]: # On ajoute la flèche du haut
                if player.saut():
                    son.son_jump.play()

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
                # Une chance sur 2  
                nb_oiseaux = random.randint(0, 1)
                for i in range(nb_oiseaux):
                    nouvel_oiseau = Mob("bird")
                    # On mets des différence (devant, derrière, au dessus, en dessous)
                    nouvel_oiseau.x += (i * random.randint(150, 300))
                    nouvel_oiseau.y_base += random.randint(-50, 50) 
                    mobs.append(nouvel_oiseau)
                spawn_timer_ciel = 0

            spawn_timer_coin += 1
            if spawn_timer_coin > (FPS * 1.8):
                hauteur_piece = random.choice([H-200, H-400, H-150])
                coins.append(Coin(L + 50, hauteur_piece))
                spawn_timer_coin = 0
        screen.fill((255, 255, 255))
        env.maj(screen)

        if not jeu_en_cours:
            Systeme.fenetre_lanceur(screen)
        else:
            player.maj(screen)
            Systeme.afficher_interface(screen, player, score)

            for c in coins[:]:
                if not player.pause:
                    c.maj(screen, multiplicateur)
                else:
                    img = Coin.images[int(c.index)]
                    screen.blit(img, (c.x, c.y))
                
                if player.hitbox.colliderect(c.hitbox):
                    son.son_coin.play()
                    score += 1
                    coins.remove(c)
                elif c.x < -100:
                    coins.remove(c)

            for m in mobs[:]:
                if not player.pause:
                    m.maj(screen, multiplicateur)
                else:
                    rect = (int(m.index) * m.w, 0, m.w, m.h)
                    screen.blit(m.image, (m.x, m.y), rect)

                if player.hitbox.colliderect(m.hitbox) and not m.touchee:
                    son.son_hit.play()
                    m.touchee = True
                    player.pointson_de_vie -= 1
                    
                if not player.pause and m.x < -200:
                    mobs.remove(m)

            if player.pause:
                Systeme.fenetre_pause(screen)

        # Custom caption pour le debug et l'info joueur
        v_actuelle = round(env.vitesse_sol, 2)
        pygame.display.set_caption(f"Get What U Need - {time.strftime('%Hh%M')} - Vitesse: {v_actuelle}")
        pygame.display.flip()
        clock.tick(FPS) # On limite les FPS (pas besoin d'aller excessivement vite, on est qu'en 2d)

if __name__ == "__main__":
    print("Lancement de l'application")
    run()
    print("Arrêt de l'application")
