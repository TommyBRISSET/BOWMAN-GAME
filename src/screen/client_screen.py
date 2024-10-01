import sys
import pygame

from multiplayer.client import Client
from game_mode.game import Game


class ClientScreen:
    """Classe représentant l'écran du client"""

    def __init__(self, game, utils, wind, wall):
        self.game = game
        self.utils = utils
        self.wind = wind
        self.wall = wall

        # Initialiser le client
        self.client = Client()

        # Initialiser les polices et les images
        self.font = None
        self.font_title = None
        self.small_font = None
        self.connect_button = None
        self.button_back_image = None
        self.back_button = None
        self.background_image = None

        self.load_images_and_fonts()

    def load_images_and_fonts(self):
        """Charger les images et les polices pour l'écran du client"""
        self.font = self.utils.load_font(self.utils.paths['font'], 36)
        self.font_title = self.utils.load_font(self.utils.paths['font'], 90)
        self.small_font = self.utils.load_font(self.utils.paths['font'], 30)
        self.connect_button = pygame.Rect(self.utils.WIDTH // 2 - 100, self.utils.HEIGHT // 2 - 50, 200, 50)
        self.button_back_image = self.utils.load_image(self.utils.paths['choose_menu_back'], (180, 110))
        self.back_button = pygame.Rect(20, 20, 100, 50)
        self.background_image = self.utils.load_image(self.utils.paths['background_menu'],
                                                      (self.utils.WIDTH, self.utils.HEIGHT))
        self.button_image = self.utils.load_image(self.utils.paths['choose_menu_start'], (430, 180))

    def display(self, running):
        """Afficher l'écran du client"""
        while running:
            self.render_screen()
            pygame.display.update()
            if self.handle_events():
                return
            if self.client.is_connected:
                self.render_waiting_for_server()
                pygame.display.update()
                if self.client.receive_message() == "START_GAME":
                    self.start_game()
            elif self.client.server_not_found:
                self.render_server_not_found()
                pygame.display.update()

    def render_screen(self):
        """Rendre l'écran du client"""
        self.game.screen.blit(self.background_image, (0, 0))
        self.render_title()
        self.render_button(self.utils.client_connect, self.connect_button)
        self.render_connection_status()
        self.game.screen.blit(self.button_back_image, (self.back_button.x - 10, self.back_button.y - 15))
        self.game.screen.blit(self.font.render(self.utils.choose_mode_back, True, self.utils.COLORS['BLACK']),
                              (self.back_button.x + 20, self.back_button.y + 15))

    def render_title(self):
        """Rendre le titre des paramètres du client"""
        title_surface = self.font_title.render(self.utils.client_title, True, self.utils.COLORS['WHITE'])
        self.game.screen.blit(title_surface, (self.utils.WIDTH // 2 - title_surface.get_width() // 2, 20))

    def render_button(self, text, button_rect):
        """Rendre un bouton avec du texte"""
        self.game.screen.blit(self.button_image, (button_rect.x - 100, button_rect.y - 50))
        button_text = self.small_font.render(text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2 + 17,
                                            button_rect.y + button_rect.height // 2 - button_text.get_height() // 2 + 7))

    def render_waiting_for_server(self):
        """Rendre le message 'En attente du serveur'"""
        waiting_surface = self.font.render(self.utils.waiting_server_txt, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(waiting_surface, (self.utils.WIDTH // 2 - waiting_surface.get_width() // 4,
                                                self.utils.HEIGHT // 2 + 20))

    def render_connection_status(self):
        """Rendre le statut de la connexion"""
        status_text = f"{self.utils.connected_to_server} : {self.client.is_connected}"
        status_surface = self.font.render(status_text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(status_surface, (self.utils.WIDTH // 2 - 150, self.utils.HEIGHT // 2 - 150))

    def render_server_not_found(self):
        """Rendre le message 'Server not found'"""
        not_found_surface = self.font.render(self.utils.server_not_found, True, self.utils.COLORS['RED'])
        self.game.screen.blit(not_found_surface, (
            self.utils.WIDTH // 2 - not_found_surface.get_width() // 2, self.utils.HEIGHT // 2 + 100))

    def handle_events(self):
        """Gérer les événements pour l'écran du client"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    return True
                if self.connect_button.collidepoint(event.pos):
                    self.client.connect_to_server()

    def start_game(self):
        """Démarrer le jeu en mode client"""
        game = Game(self.game.screen, self.game.running, self.utils, self.wind, self.wall)
        game.run_game_vs_player()
