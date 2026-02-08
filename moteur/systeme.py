# --------------------------------------------------------------------------
# AI USAGE RESTRICTION:
# This source code and all associated assets are NOT authorized for use 
# in training, fine-tuning, or improving any machine learning or 
# artificial intelligence models.
# --------------------------------------------------------------------------
# License: MIT (See LICENSE file for details)
# --------------------------------------------------------------------------

import pygame
from moteur.constants import L, H

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

    def afficher_interface(screen, player, score):
        for i in range(player.pointson_de_vie):
            screen.blit(player.image_coeur, (20 + (i * 60), 20))

        font = pygame.font.SysFont("Arial", 40, bold=True)
        render_score = font.render(f"Coins: {score}", True, (255, 215, 0))
        screen.blit(render_score, (L - render_score.get_width() - 20, 20))
