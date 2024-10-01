import sys
import pygame
from screen.customization import CustomizationScreen
from screen.choose_mode import ChooseMode
from screen.info import Info
from screen.quit_game import QuitGame


class Menu:
    """Classe pour afficher le menu principal du jeu"""

    def __init__(self, screen, running, utils):
        self.screen = screen
        self.running = running
        self.utils = utils

        # Initialise les variables pour les choix du menu
        self.info_rect = None
        self.exit_rect = None
        self.settings_rect = None
        self.play_computer_rect = None
        self.play_rect = None
        self.spacing = None
        self.banner_rects = None
        self.banner_messages = None
        self.font_title = None
        self.font = None
        self.menu_exit_image_path = None
        self.menu_choice_image_path = None
        self.deco_image = None
        self.background_menu = None

        # Initialise les constantes
        self.BANNER_SCROLL_SPEED = 8
        self.BANNER_SPACING = 2
        self.TITLE_FONT_SIZE = 100
        self.MENU_FONT_SIZE = 36
        self.DECO_IMAGE_SIZE = (1000, 200)
        self.INFO_IMAGE_SIZE = (150, 150)
        self.EXIT_IMAGE_SIZE = (140, 140)

        # Charge les images et les polices
        self.load_assets()

        # Crée les messages du bandeau
        self.create_banner_messages()

        # Initialise les rectangles des choix du menu
        self.initialize_menu_choice_rects()

    def load_assets(self):
        """Charge les images et les polices"""
        self.background_menu = self.utils.load_image(self.utils.paths['background_menu'], (self.utils.WIDTH,
                                                                                           self.utils.HEIGHT))
        self.deco_image = self.utils.load_image(self.utils.paths['deco_arrow'], self.DECO_IMAGE_SIZE)
        self.menu_choice_image_path = self.utils.paths['menu_choice_image']
        self.menu_exit_image_path = self.utils.paths['menu_panel_exit']
        self.font = self.utils.load_font(self.utils.paths['font'], self.MENU_FONT_SIZE)
        self.font_title = self.utils.load_font(self.utils.paths['font'], self.TITLE_FONT_SIZE)

    def create_banner_messages(self):
        """Crée les messages du bandeau"""
        self.banner_messages = self.utils.menu_banner
        self.banner_rects = [self.font.render(msg, True, (0, 0, 0)).get_rect() for msg in self.banner_messages]
        for i, rect in enumerate(self.banner_rects):
            rect.topleft = (self.utils.WIDTH + i * self.utils.WIDTH // self.BANNER_SPACING, 10)
        self.spacing = self.utils.WIDTH // self.BANNER_SPACING

    def initialize_menu_choice_rects(self):
        """Initialise les rectangles des choix du menu"""
        self.play_rect = self.create_choice_rect(self.utils.menu_player, self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2.8)
        self.play_computer_rect = self.create_choice_rect(self.utils.menu_computer, self.screen.get_width() // 2,
                                                          self.screen.get_height() // 2.1)
        self.settings_rect = self.create_choice_rect(self.utils.menu_settings, self.screen.get_width() // 2,
                                                     self.screen.get_height() // 1.65)

    def create_choice_rect(self, text, x, y):
        """Crée un rectangle pour un choix du menu"""
        choice_text = self.font.render(text, True, self.utils.COLORS['BLACK'])
        choice_rect = choice_text.get_rect(center=(x, y))
        return choice_rect

    def show_menu(self):
        """Affiche le menu principal"""
        while self.running:
            self.screen.blit(self.background_menu, (0, 0))  # Afficher l'image de fond
            self.screen.blit(self.deco_image, (self.screen.get_width() // 2 - 500, self.screen.get_height() // 6))
            self.blit_title()
            self.blit_banner_messages()  # Affiche les messages du bandeau
            self.blit_menu_choices()  # Affiche les choix du menu
            self.menu_handle_events()  # Gére les événements du menu principal
            pygame.display.flip()  # Met à jour l'écran

    def blit_title(self):
        """Méthode pour afficher le titre du jeu"""
        title_text = self.font_title.render('BOWMAN', True, self.utils.COLORS['WHITE'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 5.5))
        self.screen.blit(title_text, title_rect)

    def blit_banner_messages(self):
        """Méthode pour afficher les messages du bandeau"""
        for i, msg in enumerate(self.banner_messages):
            text = self.font.render(msg, True, (0, 0, 0))
            self.screen.blit(text, self.banner_rects[i])
            self.banner_rects[i].move_ip(-self.BANNER_SCROLL_SPEED, 0)
            # Si le dernier message est sorti de l'écran
            if i == len(self.banner_messages) - 1 and self.banner_rects[i].right < 0:
                for j, rect in enumerate(self.banner_rects):  # Réinitialise la position de tous les messages
                    rect.left = self.utils.WIDTH + j * self.spacing

    def blit_menu_choices(self):
        """Méthode pour afficher les choix du menu"""
        self.blit_choice(self.utils.menu_player, self.screen.get_width() // 2, self.screen.get_height() // 2.8)
        self.blit_choice(self.utils.menu_computer, self.screen.get_width() // 2, self.screen.get_height() // 2.1)
        self.blit_choice(self.utils.menu_settings, self.screen.get_width() // 2, self.screen.get_height() // 1.65)
        self.blit_exit_button()
        self.blit_info_choice()

    def blit_choice(self, text, x, y):
        """Méthode pour afficher un choix du menu"""
        choice_text = self.font.render(text, True, self.utils.COLORS['BLACK'])
        choice_rect = choice_text.get_rect(center=(x, y))
        choice_image = self.utils.load_image(self.menu_choice_image_path, (choice_rect.width + 330,
                                                                           choice_rect.height + 70))
        self.screen.blit(choice_image, (choice_rect.x - 160, choice_rect.y - 17))
        self.screen.blit(choice_text, choice_rect)

    def blit_exit_button(self):
        """Méthode pour afficher le bouton "Exit"""
        exit_text = self.font.render(self.utils.menu_exit, True, self.utils.COLORS['BLACK'])
        self.exit_rect = exit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 1.4))
        exit_image = self.utils.load_image(self.menu_exit_image_path, (self.exit_rect.width + self.EXIT_IMAGE_SIZE[0],
                                                                       self.exit_rect.height + self.EXIT_IMAGE_SIZE[1]))
        self.screen.blit(exit_image, (self.exit_rect.x - 70, self.exit_rect.y - 63))
        self.screen.blit(exit_text, self.exit_rect)

    def blit_info_choice(self):
        """Méthode pour afficher le choix d'information"""
        info_image = self.utils.load_image(self.utils.paths['info'], self.INFO_IMAGE_SIZE)
        self.info_rect = pygame.Rect(0, self.screen.get_height() - info_image.get_height(), info_image.get_width(),
                                     info_image.get_height())
        self.screen.blit(info_image, (self.info_rect.x, self.info_rect.y))

    def menu_handle_events(self):
        """Méthode pour gérer les événements du menu principal"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game = QuitGame(self.screen, self.running, self.utils)
                    quit_game.display()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Méthode pour gérer le clic de la souris"""
        if self.play_rect.collidepoint(pos):
            choose_mode = ChooseMode(self, self.utils, vs_computer=False, vs_player=True, online=True)
            choose_mode.display()
        elif self.play_computer_rect.collidepoint(pos):
            choose_mode = ChooseMode(self, self.utils, vs_computer=True, vs_player=False, online=False)
            choose_mode.display()
        elif self.settings_rect.collidepoint(pos):
            CustomizationScreen(self.screen, self.running, self.utils).display_customization_screen()
        elif self.info_rect.collidepoint(pos):
            info = Info(self.utils, self.screen, self.running)
            info.run()
        elif self.exit_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()
