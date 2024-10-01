import sys

import pygame


class QuitGame:
    """Classe pour quitter le jeu"""
    def __init__(self, screen, running, utils):
        self.screen = screen
        self.running = running
        self.utils = utils

        # Charge les polices
        self.font = self.utils.load_font(self.utils.paths['font'], 36)
        self.font_title = self.utils.load_font(self.utils.paths['font'], 48)

        self.menu_box = pygame.Rect(self.utils.WIDTH // 2 - 300, self.utils.HEIGHT // 2 - 275, 625, 525)

        # Charge les images
        self.menu_box_image = self.utils.load_image(self.utils.paths['quit_game'], (625, 525))
        self.button_image = self.utils.load_image(self.utils.paths['button_break'], (300, 175))

        # Boutons
        self.yes_button = pygame.Rect(self.menu_box.x + 185, self.menu_box.y + 225, 200, 50)
        self.no_button = pygame.Rect(self.menu_box.x + 175, self.menu_box.y + 300, 220, 50)

        # Crée une surface semi-transparente
        self.overlay = pygame.Surface((self.utils.WIDTH, self.utils.HEIGHT))
        self.overlay.set_alpha(30)
        self.overlay.fill(self.utils.COLORS['GRAY'])

    def display(self):
        """Affiche le menu de pause"""
        while True:
            self.render_screen()
            pygame.display.update()
            if self.handle_events():
                return

    def render_screen(self):
        """Rendre l'écran"""
        self.screen.blit(self.overlay, (0, 0))  # Affiche la surface semi-transparente
        self.screen.blit(self.menu_box_image, (self.menu_box.x, self.menu_box.y))

        quit_game_title = self.font_title.render(self.utils.quit_game_title, True, self.utils.COLORS['BLACK'])
        self.screen.blit(quit_game_title, (self.menu_box.x + self.menu_box.width // 2 - quit_game_title.get_width()
                                           // 2, self.menu_box.y + 110))

        # Affiche les images des boutons
        self.screen.blit(self.button_image, (self.yes_button.x - 50, self.yes_button.y - 55))
        self.screen.blit(self.button_image, (self.no_button.x - 40, self.no_button.y - 45))

        self.render_button_text(self.utils.yes, self.yes_button)
        self.render_button_text(self.utils.no, self.no_button, y_offset=10)

    def render_button_text(self, text, button_rect, y_offset=0):
        """Rendre le texte du bouton"""
        button_text = self.font.render(text, True, self.utils.COLORS['BLACK'])
        self.screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                       button_rect.y + y_offset))

    def handle_events(self):
        """Gére les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle_mouse_click(event.pos):
                    return True

    def handle_mouse_click(self, pos):
        """Gére le clic de la souris"""
        if self.yes_button.collidepoint(pos):
            pygame.quit()
            sys.exit()
        elif self.no_button.collidepoint(pos):
            return True
