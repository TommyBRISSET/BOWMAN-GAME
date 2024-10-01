import pygame


class BreakMenu:
    """Classe pour le menu de pause"""
    def __init__(self, game, utils):
        self.game = game
        self.utils = utils

        # Charge les polices
        self.font = self.utils.load_font(self.utils.paths['font'], 36)
        self.font_title = self.utils.load_font(self.utils.paths['font'], 48)

        self.menu_box = pygame.Rect(self.utils.WIDTH // 2 - 255, self.utils.HEIGHT // 2 - 275, 510, 550)

        # Charge les images
        self.menu_box_image = self.utils.load_image(self.utils.paths['menu_break_box'], (510, 550))
        self.button_image = self.utils.load_image(self.utils.paths['button_break'], (300, 175))

        # Boutons
        self.resume_button = pygame.Rect(self.menu_box.x + 155, self.menu_box.y + 225, 200, 50)
        self.menu_button = pygame.Rect(self.menu_box.x + 145, self.menu_box.y + 300, 220, 50)

    def display(self):
        """Affiche le menu de pause"""
        while True:
            self.render_screen()
            pygame.display.update()
            if self.handle_events():
                return

    def render_screen(self):
        """Affiche les éléments du menu de pause"""
        self.game.screen.blit(self.menu_box_image, (self.menu_box.x, self.menu_box.y))

        break_text = self.font_title.render(self.utils.break_menu_title, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(break_text, (self.menu_box.x + self.menu_box.width // 2 - break_text.get_width() // 2,
                                           self.menu_box.y + 110))

        # Affiche les images des boutons
        self.game.screen.blit(self.button_image, (self.resume_button.x - 50, self.resume_button.y - 55))
        self.game.screen.blit(self.button_image, (self.menu_button.x - 40, self.menu_button.y - 45))

        self.render_button_text(self.utils.break_menu_resume, self.resume_button)
        self.render_button_text(self.utils.break_menu_menu, self.menu_button, y_offset=10)

    def render_button_text(self, text, button_rect, y_offset=0):
        """Rendre le texte du bouton"""
        button_text = self.font.render(text, True, self.utils.COLORS['BLACK'])
        self.game.screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                            button_rect.y + y_offset))

    def handle_events(self):
        """Gérer les événements"""
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
        self.game.clock.tick(60)

    def handle_mouse_click(self, pos):
        """Gére le clic de la souris"""
        if self.resume_button.collidepoint(pos):
            return True
        elif self.menu_button.collidepoint(pos):
            self.go_to_menu()
            return True

    def go_to_menu(self):
        """Méthode pour retourner au menu principal"""
        from screen.menu import Menu
        menu = Menu(self.game.screen, True, self.utils)
        menu.show_menu()
