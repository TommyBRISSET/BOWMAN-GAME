import sys
import pygame
from pygame.locals import *
from game_mode.game import Game
from screen.client_screen import ClientScreen
from screen.server_screen import ServerScreen


class ChooseMode:
    """Classe pour afficher le menu de choix du mode de jeu et des options"""
    def __init__(self, game, utils, vs_computer, vs_player, online):
        self.game = game
        self.utils = utils
        self.vs_computer = vs_computer
        self.vs_player = vs_player
        self.online = online
        self.online_available = self.online

        # Initialiser les variables pour les choix du menu
        self.back_button = None
        self.start_button = None
        self.client_checkbox = None
        self.server_checkbox = None
        self.wall_checkbox = None
        self.wind_checkbox = None
        self.online_checkbox = None
        self.local_checkbox = None
        self.start_image = None
        self.button_back_image = None
        self.background = None
        self.title = None
        self.font_title = None
        self.font = None

        # Charger les images et les polices
        self.load_assets_and_initialize()
        self.load_checkbox_rects()

        # Initialiser les variables pour les options
        self.local = True
        self.online = False
        self.wind = False
        self.wall = False
        self.server = True
        self.client = False

    def load_assets_and_initialize(self):
        """Charge les images et les polices"""
        self.font = self.utils.load_font(self.utils.paths['font'], 36)
        self.font_title = self.utils.load_font(self.utils.paths['font'], 100)
        self.title = self.font_title.render(self.utils.choose_mode_title, True, self.utils.COLORS['BLACK'])
        self.background = self.utils.load_image(self.utils.paths['background_menu'],
                                                (self.utils.WIDTH, self.utils.HEIGHT))
        self.button_back_image = self.utils.load_image(self.utils.paths['choose_menu_back'], (180, 110))
        self.start_image = self.utils.load_image(self.utils.paths['choose_menu_start'], (390, 170))

    def load_checkbox_rects(self):
        """Initialise les rectangles des cases à cocher"""
        self.local_checkbox = pygame.Rect(self.utils.WIDTH // 2 - 250, self.utils.HEIGHT // 2 - 100, 50, 50)
        self.online_checkbox = pygame.Rect(self.utils.WIDTH // 2 + 150, self.utils.HEIGHT // 2 - 100, 50, 50)
        self.wind_checkbox = pygame.Rect(self.utils.WIDTH // 2 - 250, self.utils.HEIGHT // 2, 50, 50)
        self.wall_checkbox = pygame.Rect(self.utils.WIDTH // 2 + 150, self.utils.HEIGHT // 2, 50, 50)
        self.server_checkbox = pygame.Rect(self.utils.WIDTH // 2 - 250, self.utils.HEIGHT // 2 + 100, 50, 50)
        self.client_checkbox = pygame.Rect(self.utils.WIDTH // 2 + 150, self.utils.HEIGHT // 2 + 100, 50, 50)
        self.start_button = pygame.Rect(self.utils.WIDTH // 2 - 100, self.utils.HEIGHT - 100, 210, 50)
        self.back_button = pygame.Rect(20, 20, 100, 50)

    def display(self):
        """Méthode pour afficher le menu de choix du mode de jeu et des options"""
        while True:
            if self.handle_events():
                return
            self.render_screen()
            pygame.display.update()

    def handle_events(self):
        """Gére les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
                if self.back_button.collidepoint(event.pos):
                    return True

    def handle_mouse_click(self, pos):
        """Gére le clic de la souris"""
        if self.local_checkbox.collidepoint(pos):
            self.local = not self.local
            self.online = not self.local
        elif self.wind_checkbox.collidepoint(pos):
            self.wind = not self.wind
        elif self.wall_checkbox.collidepoint(pos):
            self.wall = not self.wall
        elif self.start_button.collidepoint(pos):
            self.start_game()
        if self.online_available:
            if self.online_checkbox.collidepoint(pos):
                self.online = not self.online
                self.local = not self.online
            if self.online:
                if self.server_checkbox.collidepoint(pos):
                    self.server = not self.server
                    self.client = False
                elif self.client_checkbox.collidepoint(pos):
                    self.client = not self.client
                    self.server = False

    def render_checkbox_text(self, text, rect):
        """Méthode pour afficher le texte à côté de la case à cocher"""
        self.game.screen.blit(self.font.render(text, True, self.utils.COLORS['BLACK']), (rect.x + 60, rect.y))

    def render_screen(self):
        """Méthode pour rendre l'écran"""
        self.game.screen.blit(self.background, (0, 0))  # Display the background image
        self.game.screen.blit(self.title, (self.utils.WIDTH // 2 - self.title.get_width() // 2,
                                           self.utils.HEIGHT // 5 - 200))

        # Affichage des rectangles pour les cases à cocher
        self.draw_checkbox(self.local_checkbox, self.local)
        self.draw_checkbox(self.wind_checkbox, self.wind)
        self.draw_checkbox(self.wall_checkbox, self.wall)

        # Affichage des images et des textes
        self.game.screen.blit(self.start_image, (self.start_button.x - 95, self.start_button.y - 50))
        self.game.screen.blit(self.button_back_image, (self.back_button.x - 10, self.back_button.y - 15))

        self.render_checkbox_text(self.utils.choose_mode_local, self.local_checkbox)
        if self.online_available:
            self.draw_checkbox(self.online_checkbox, self.online)
            self.render_checkbox_text(self.utils.choose_mode_online, self.online_checkbox)
            if self.online:
                self.draw_checkbox(self.server_checkbox, self.server)
                self.draw_checkbox(self.client_checkbox, self.client)
                self.render_checkbox_text(self.utils.choose_server, self.server_checkbox)
                self.render_checkbox_text(self.utils.choose_client, self.client_checkbox)

        self.render_checkbox_text(self.utils.choose_mode_wind, self.wind_checkbox)
        self.render_checkbox_text(self.utils.choose_mode_wall, self.wall_checkbox)
        self.game.screen.blit(self.font.render(self.utils.choose_mode_start, True, self.utils.COLORS['BLACK']),
                              (self.start_button.x, self.start_button.y))
        self.game.screen.blit(self.font.render(self.utils.choose_mode_back, True, self.utils.COLORS['BLACK']),
                              (self.back_button.x + 20, self.back_button.y + 15))

    def draw_checkbox(self, rect, checked):
        """Méthode pour dessiner une case à cocher"""
        pygame.draw.rect(self.game.screen, self.utils.COLORS['BLACK'], rect, 4)
        if checked:
            pygame.draw.line(self.game.screen, self.utils.COLORS['BLACK'], rect.topleft, rect.bottomright, 4)
            pygame.draw.line(self.game.screen, self.utils.COLORS['BLACK'], rect.topright, rect.bottomleft, 4)

    def start_game(self):
        """Méthode pour démarrer le jeu avec les options choisies"""
        game = Game(self.game.screen, self.game.running, self.utils, self.wind, self.wall)
        if self.vs_player:
            if self.local:
                game.run_game_vs_player()
            else:
                if self.online:
                    if self.server:
                        server_screen = ServerScreen(game, self.utils, self.wind, self.wall)
                        server_screen.display(self.game.running)
                    elif self.client:
                        client_screen = ClientScreen(game, self.utils, self.wind, self.wall)
                        client_screen.display(self.game.running)
        elif self.vs_computer:
            if self.local:
                game.run_game_vs_computer()
