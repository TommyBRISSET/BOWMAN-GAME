import sys
import pygame
import webbrowser


class Info:
    """ Classe pour l'écran d'information"""
    def __init__(self, utils, screen, running):
        self.utils = utils
        self.screen = screen
        self.running = running

        self.FONT_SIZE = 36
        self.LINK_URL = 'https://github.com/TommyBRISSET/BOWMAN'

        # Charge les polices
        self.font = self.utils.load_font(self.utils.paths['font'], self.FONT_SIZE)
        self.font_bold = self.utils.load_font(self.utils.paths['font'], self.FONT_SIZE)
        self.font_bold.set_bold(True)

        print(self.utils.WIDTH, self.utils.HEIGHT)
        self.menu_box = pygame.Rect(utils.WIDTH // 2 - 255, utils.HEIGHT // 2 - 275, 810, 740)

        # Charge les images
        self.menu_box_image = self.utils.load_image(self.utils.paths['menu_break_box'], (810, 740))

        # Crée les textes
        self.text = self.font.render(self.utils.info_text, True, self.utils.COLORS['BLACK'])
        self.link_text = self.font_bold.render(self.utils.info_link, True, self.utils.COLORS['BLACK'])
        self.version_text = self.font.render(self.utils.info_version, True, self.utils.COLORS['BLACK'])
        self.made_by_text = self.font.render(self.utils.info_made_by, True, self.utils.COLORS['BLACK'])

        # Crée les rectangles pour les textes
        self.text_rect = self.text.get_rect(center=(utils.WIDTH // 2, utils.HEIGHT // 2 - 100))
        self.link_rect = self.link_text.get_rect(center=(utils.WIDTH // 2, utils.HEIGHT // 2))
        self.version_rect = self.version_text.get_rect(center=(utils.WIDTH // 2, utils.HEIGHT // 2 + 100))
        self.made_by_rect = self.made_by_text.get_rect(center=(utils.WIDTH // 2, utils.HEIGHT // 2 + 200))

    def run(self):
        """ Affiche l'écran d'information"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.link_rect.collidepoint(mouse_pos):
                        webbrowser.open(self.LINK_URL)
                    elif not self.menu_box.collidepoint(mouse_pos):
                        return

            self.draw_screen()

    def draw_screen(self):
        """Dessine l'écran"""
        self.screen.blit(self.menu_box_image, (self.menu_box.x - 160, self.menu_box.y - 50))
        self.screen.blit(self.text, self.text_rect)
        self.screen.blit(self.link_text, self.link_rect)
        self.screen.blit(self.version_text, self.version_rect)
        self.screen.blit(self.made_by_text, self.made_by_rect)
        pygame.display.flip()
