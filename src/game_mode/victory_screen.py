import sys
import pygame


class VictoryScreen:
    """Écran de victoire"""
    def __init__(self, screen, utils, time):
        self.screen = screen
        self.utils = utils
        self.time = time
        self.replay = None

        self.menu_box = pygame.Rect(self.utils.WIDTH // 2 - 330, self.utils.HEIGHT // 2 - 370, 650, 680)

        # Charge les images
        self.menu_box_image = self.utils.load_image(self.utils.paths['menu_break_box'], (650, 680))
        self.button_image = self.utils.load_image(self.utils.paths['button_break'], (320, 185))
        self.trophy_image = self.utils.load_image(self.utils.paths['victory_trophy'], (240, 140))

        # Boutons
        self.replay_button = pygame.Rect(self.utils.WIDTH // 2 - 100, self.utils.HEIGHT // 2, 250, 100)
        self.menu_button = pygame.Rect(self.utils.WIDTH // 2 - 110, self.utils.HEIGHT // 1.68, 250, 100)

        # Polices
        self.font = self.utils.load_font(self.utils.paths['font'], 48)
        self.small_font = self.utils.load_font(self.utils.paths['font'], 36)

    def display(self, winner, running):
        """Affiche l'écran de victoire"""
        while running:
            self.render_screen(winner)
            pygame.display.update()
            self.handle_events()
            if self.replay == 'replay':
                return 'replay'

    def render_screen(self, winner):
        """Rendre l'écran"""
        self.screen.blit(self.menu_box_image, (self.menu_box.x, self.menu_box.y))
        self.screen.blit(self.trophy_image, (self.utils.WIDTH // 2 - 110, self.utils.HEIGHT // 3.4))

        victory_text = self.font.render(f"{winner} Wins !", True, self.utils.COLORS['BLACK'])
        victory_rect = victory_text.get_rect(center=(self.utils.WIDTH // 2, self.utils.HEIGHT // 3.6))
        self.screen.blit(victory_text, victory_rect)

        self.screen.blit(self.button_image, (self.replay_button.x - 40, self.replay_button.y - 55))
        self.screen.blit(self.button_image, (self.menu_button.x - 40, self.menu_button.y - 50))

        self.render_button_text("Replay", self.replay_button)
        self.render_button_text("Main Menu", self.menu_button, y_offset=10)
        self.render_timer()

    def render_button_text(self, text, button_rect, y_offset=0):
        """Rendre le texte du bouton"""
        button_text = self.small_font.render(text, True, self.utils.COLORS['BLACK'])
        self.screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                       button_rect.y + y_offset))

    def render_timer(self):
        """Rendre le timer"""
        elapsed_time = self.time
        time_text = self.small_font.render(f"{self.utils.elapsed_time} {elapsed_time}", True,
                                           self.utils.COLORS['BLACK'])
        self.screen.blit(time_text, (self.utils.WIDTH // 2.5, self.utils.HEIGHT // 2.4))

    def handle_events(self):
        """Gérer les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.replay_button.collidepoint(event.pos):
                    self.replay = 'replay'
                    return True
                elif self.menu_button.collidepoint(event.pos):
                    self.go_to_menu()
                    return True

    def go_to_menu(self):
        """Méthode pour retourner au menu principal"""
        from screen.menu import Menu
        menu = Menu(self.screen, True, self.utils)
        menu.show_menu()
