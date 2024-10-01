import pygame
import sys
from multiplayer.server import Server
from game_mode.game import Game


class ServerScreen:
    """Écran pour afficher les contrôles et le statut du serveur"""

    def __init__(self, game, utils, wind, wall):
        self.game = game
        self.utils = utils
        self.wind = wind
        self.wall = wall

        # Initialiser le serveur
        self.server = Server()

        # Initialiser les variables
        self.background_menu = None
        self.font_title = None
        self.font = None
        self.start_server_button = None
        self.stop_server_button = None
        self.start_game_button = None
        self.button_back_image = None
        self.back_button = None

        self.load_assets_and_initialize()

    def load_assets_and_initialize(self):
        """Charger les images et les polices"""
        self.font = self.utils.load_font(self.utils.paths['font'], 36)
        self.font_title = self.utils.load_font(self.utils.paths['font'], 90)
        self.small_font = self.utils.load_font(self.utils.paths['font'], 30)
        self.start_image = self.utils.load_image(self.utils.paths['choose_menu_start'], (380, 160))
        self.background_menu = self.utils.load_image(self.utils.paths['background_menu'],
                                                     (self.utils.WIDTH, self.utils.HEIGHT))
        self.start_server_button = pygame.Rect(self.utils.WIDTH // 2 - 150, self.utils.HEIGHT // 2 - 150, 300, 100)
        self.stop_server_button = pygame.Rect(self.utils.WIDTH // 2 - 150, self.utils.HEIGHT // 2 - 50, 300, 100)
        self.start_game_button = pygame.Rect(self.utils.WIDTH // 2 - 150, self.utils.HEIGHT // 2 + 50, 300, 100)
        self.button_back_image = self.utils.load_image(self.utils.paths['choose_menu_back'], (180, 110))
        self.back_button = pygame.Rect(20, 20, 100, 50)

    def display(self, running):
        """Afficher l'écran du serveur"""
        while running:
            self.render_screen()
            pygame.display.update()
            if self.handle_events():
                return
            if self.server.client_connected:
                self.render_client_status()

    def render_screen(self):
        """Rendre l'écran du serveur"""
        self.game.screen.blit(self.background_menu, (0, 0))
        self.render_title()
        self.render_button(self.utils.start_server, self.start_server_button)
        self.render_button(self.utils.stop_server, self.stop_server_button)
        if self.server.client_connected:
            self.render_button(self.utils.choose_mode_start, self.start_game_button)
        self.render_server_status()
        self.render_server_ip_port()
        self.render_client_waiting_status()
        self.game.screen.blit(self.button_back_image, (self.back_button.x - 10, self.back_button.y - 15))
        self.game.screen.blit(self.font.render(self.utils.choose_mode_back, True, self.utils.COLORS['BLACK']),
                              (self.back_button.x + 20, self.back_button.y + 15))

    def render_title(self):
        """Rendre le titre des paramètres du serveur"""
        title_surface = self.font_title.render(self.utils.server_title, True, self.utils.COLORS['WHITE'])
        self.game.screen.blit(title_surface, (self.utils.WIDTH // 2 - title_surface.get_width() // 2, 20))

    def render_button(self, text, button_rect):
        """Rendre un bouton avec du texte"""
        self.game.screen.blit(self.start_image, (button_rect.x - 20 , button_rect.y - 20))
        button_text = self.small_font.render(text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2 + 17,
                                            button_rect.y + button_rect.height // 2 - button_text.get_height() // 2 + 7))

    def render_server_status(self):
        """Rendre le statut du serveur"""
        status_text = f"{self.utils.server_running} : {self.server.is_running}"
        color = self.utils.COLORS['GREEN'] if self.server.is_running else self.utils.COLORS['RED']
        status_surface = self.font.render(status_text, True, color)
        self.game.screen.blit(status_surface,
                              (self.utils.WIDTH // 2 - status_surface.get_width() // 2, self.utils.HEIGHT // 2 - 250))

    def render_client_status(self):
        """Rendre le statut de la connexion client"""
        client_text = f"{self.utils.client_connected} : {self.server.client_connected}"
        client_color = self.utils.COLORS['GREEN'] if self.server.client_connected else self.utils.COLORS['BLACK']
        client_surface = self.font.render(client_text, True, client_color)
        self.game.screen.blit(client_surface, (50, self.utils.HEIGHT // 2 - 100))

    def render_server_ip_port(self):
        """Rendre l'IP et le port du serveur"""
        ip_port_text = f"{self.utils.IP}{self.server.ip} {self.utils.port}{self.server.port}"
        ip_port_surface = self.font.render(ip_port_text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(ip_port_surface, (50, self.utils.HEIGHT // 2 - 200))

    def render_client_waiting_status(self):
        """Rendre le statut d'attente du client"""
        if not self.server.client_connected:
            waiting_text = self.utils.client_waiting
        else:
            waiting_text = f"{self.utils.client_ip} : {self.server.client_address[0]}"
        waiting_surface = self.font.render(waiting_text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(waiting_surface, (50, self.utils.HEIGHT // 2 - 50))

    def handle_events(self):
        """Gérer les événements pour l'écran du serveur"""
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
                if self.start_server_button.collidepoint(event.pos):
                    self.server.start_server()
                if self.stop_server_button.collidepoint(event.pos):
                    self.server.stop_server()
                if self.start_game_button.collidepoint(event.pos):
                    if self.server.client_connected:
                        self.start_game()
                    else:
                        pass

    def start_game(self):
        """Démarrer le jeu en mode serveur et envoyer le signal au client"""
        self.server.send_message("START_GAME")
        game = Game(self.game.screen, self.game.running, self.utils, self.wind, self.wall)
        game.run_game_vs_player()
