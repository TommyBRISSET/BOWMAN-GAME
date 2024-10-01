import pygame
import os


class CustomizationScreen:
    """Écran de personnalisation des paramètres du jeu"""

    def __init__(self, screen, running, utils):
        self.screen = screen
        self.running = running
        self.utils = utils

        # Initialisation des paramètres de personnalisation
        self.back_button_rect = None
        self.sound_toggle_rect = None
        self.lang_set_rects = None
        self.wall_skin_rects = None
        self.background_skin_rects = None
        self.arrow_skin_rects = None
        self.archer_skin_rects = None
        self.font_title = None
        self.font = None
        self.background_menu = None
        self.current_lang_set = None
        self.current_wall_skin = None
        self.current_background_skin = None
        self.current_arrow_skin = None
        self.current_archer_skin = None
        self.back_image_custo = None
        self.sound_off_image = None
        self.sound_on_image = None
        self.lang_set = None
        self.wall_skins = None
        self.background_colors = None
        self.arrow_skins = None
        self.archer_skins = None
        self.right_arrow_lang = None
        self.left_arrow_wall = None
        self.left_arrow_lang = None
        self.right_arrow_wall = None
        self.right_arrow_background = None
        self.left_arrow_background = None
        self.left_arrow_arrow = None
        self.right_arrow_arrow = None
        self.right_arrow_archer = None
        self.left_arrow_archer = None

        # Initialisation des constantes
        self.FONT_SIZE = 36
        self.TITLE_FONT_SIZE = 72
        self.SKIN_SIZE = (125, 110)
        self.ARROW_SIZE = (125, 100)
        self.WALL_SIZE = (125, 125)
        self.LANG_SIZE = (125, 125)
        self.SOUND_SIZE = (150, 150)
        self.BACK_BUTTON_SIZE = (490, 170)

        # Initialisation des pages pour chaque rangée
        self.current_page_archer = 0
        self.current_page_arrow = 0
        self.current_page_background = 0
        self.current_page_wall = 0
        self.current_page_lang = 0
        self.items_per_page = 5

        # Chargement des flèches
        self.left_arrow_image = self.utils.load_image(self.utils.paths["left_arrow"], (50, 50))
        self.right_arrow_image = self.utils.load_image(self.utils.paths["right_arrow"], (50, 50))

        self.base_path = self.utils.get_base_path()

        self.load_assets()
        self.init_active_skins()
        self.load_font_and_background()

    def load_assets(self):
        """Charge les images pour les skins des archers, des flèches, des fonds et des murs"""
        archer_skin_dir = self.base_path + '/archer_skin/'
        arrow_skin_dir = self.base_path + '/arrow_skin/'
        wall_skin_dir = self.base_path + '/wall_skin/'
        lang_set_dir = self.base_path + '/lang_set/'

        self.archer_skins = [self.utils.load_image(os.path.join(archer_skin_dir, file), self.SKIN_SIZE)
                             for file in os.listdir(archer_skin_dir) if file.endswith('.png')]
        self.arrow_skins = [self.utils.load_image(os.path.join(arrow_skin_dir, file), self.ARROW_SIZE)
                            for file in os.listdir(arrow_skin_dir) if file.endswith('.png')]
        self.wall_skins = [self.utils.load_image(os.path.join(wall_skin_dir, file), self.WALL_SIZE)
                           for file in os.listdir(wall_skin_dir) if file.endswith('.png')]
        self.lang_set = [self.utils.load_image(os.path.join(lang_set_dir, file), self.LANG_SIZE)
                         for file in os.listdir(lang_set_dir) if file.endswith('.png')]

        self.background_colors = [self.utils.COLORS["WHITE"], self.utils.COLORS["LIGHT_YELLOW"],
                                  self.utils.COLORS["LIGHT_BLUE"], self.utils.COLORS["GRAY"],
                                  self.utils.COLORS["BEIGE"], self.utils.COLORS["DARK_BLUE"],
                                  self.utils.COLORS["LIGHT_GREEN"], self.utils.COLORS["DARK_GREEN"]]
        self.sound_on_image = self.utils.load_image(self.utils.paths["sound_img_sound_on"], self.SOUND_SIZE)
        self.sound_off_image = self.utils.load_image(self.utils.paths["sound_img_sound_off"], self.SOUND_SIZE)
        self.back_image_custo = self.utils.load_image(self.utils.paths["choose_menu_start"], self.BACK_BUTTON_SIZE)

    def init_active_skins(self):
        """Initialise les skins actuels"""
        self.current_archer_skin = self.utils.archer_skin
        self.current_arrow_skin = self.utils.arrow_skin
        self.current_background_skin = self.utils.background_skin
        self.current_wall_skin = self.utils.wall_skin
        self.current_lang_set = self.utils.lang_set

    def load_font_and_background(self):
        """Charge les polices et l'arrière-plan"""
        self.background_menu = self.utils.load_image(self.utils.paths['background_menu'],
                                                     (self.utils.WIDTH, self.utils.HEIGHT))
        self.font = self.utils.load_font(self.utils.paths['font'], self.FONT_SIZE)
        self.font_title = self.utils.load_font(self.utils.paths['font'], self.TITLE_FONT_SIZE)

    def display_customization_screen(self):
        """Méthode pour afficher l'écran de personnalisation des paramètres du jeu"""
        self.create_skin_rects()
        while self.running:
            self.screen.blit(self.background_menu, (0, 0))
            self.blit_title()
            self.blit_skins()
            self.blit_sound_toggle()
            self.blit_back_button()
            if self.handle_events():
                return
            pygame.display.update()

    def create_skin_rects(self):
        """Crée les rectangles pour les skins"""
        self.archer_skin_rects = [pygame.Rect(self.utils.WIDTH // 15 + i * 150, self.utils.HEIGHT // 3.5,
                                              *self.SKIN_SIZE) for i in
                                  range(min(self.items_per_page, len(self.archer_skins)))]
        self.arrow_skin_rects = [pygame.Rect(self.utils.WIDTH // 1.7 - 100 + i * 150, self.utils.HEIGHT // 3.5,
                                             *self.ARROW_SIZE) for i in
                                 range(min(self.items_per_page, len(self.arrow_skins)))]
        self.background_skin_rects = [pygame.Rect(self.utils.WIDTH // 15 + i * 150, self.utils.HEIGHT // 1.9, 125,
                                                  125) for i in
                                      range(min(self.items_per_page, len(self.background_colors)))]
        self.wall_skin_rects = [pygame.Rect(self.utils.WIDTH // 1.7 - 100 + i * 150, self.utils.HEIGHT // 2,
                                            *self.WALL_SIZE) for i in
                                range(min(self.items_per_page, len(self.wall_skins)))]
        self.lang_set_rects = [pygame.Rect(self.utils.WIDTH // 2 + i * 150, self.utils.HEIGHT // 1.4,
                                           *self.LANG_SIZE) for i in
                               range(min(self.items_per_page, len(self.lang_set)))]
        self.sound_toggle_rect = pygame.Rect(self.utils.WIDTH // 4 - 60, self.utils.HEIGHT // 1.4, *self.SOUND_SIZE)
        self.back_button_rect = pygame.Rect(self.utils.WIDTH // 2 - 135, self.utils.HEIGHT - 100, 350, 100)

    def blit_title(self):
        """Affiche le titre"""
        title_text = self.font_title.render(self.utils.custo_title, True, self.utils.COLORS['WHITE'])
        title_rect = title_text.get_rect(center=(self.utils.WIDTH // 2, self.utils.HEIGHT // 10))
        self.screen.blit(title_text, title_rect)

    def blit_skins(self):
        """Affiche les skins"""
        self.left_arrow_archer, self.right_arrow_archer = self.blit_skin_section(
            self.utils.custo_archer, self.archer_skins, self.archer_skin_rects,
            self.current_archer_skin, self.utils.WIDTH // 4 - 100, self.utils.HEIGHT // 5, self.current_page_archer)
        self.left_arrow_arrow, self.right_arrow_arrow = self.blit_skin_section(
            self.utils.custo_arrow, self.arrow_skins, self.arrow_skin_rects,
            self.current_arrow_skin, self.utils.WIDTH // 1.3 - 200, self.utils.HEIGHT // 5, self.current_page_arrow)
        self.left_arrow_background, self.right_arrow_background = self.blit_skin_section(
            self.utils.custo_background, self.background_colors, self.background_skin_rects,
            self.current_background_skin, self.utils.WIDTH // 4 - 100, self.utils.HEIGHT // 2.3,
            self.current_page_background, is_color=True)
        self.left_arrow_wall, self.right_arrow_wall = self.blit_skin_section(
            self.utils.custo_wall, self.wall_skins, self.wall_skin_rects, self.current_wall_skin,
            self.utils.WIDTH // 1.3 - 200, self.utils.HEIGHT // 2.3, self.current_page_wall)
        self.left_arrow_lang, self.right_arrow_lang = self.blit_skin_section(
            self.utils.custo_lang, self.lang_set, self.lang_set_rects, self.current_lang_set,
            self.utils.WIDTH // 1.5 - 80, self.utils.HEIGHT // 1.6, self.current_page_lang)

    def blit_skin_section(self, title, skins, rects, current_skin, x, y, current_index, is_color=False):
        """Affiche une section de skins"""
        section_text = self.font.render(title, True, self.utils.COLORS['BLACK'])
        self.screen.blit(section_text, (x, y))
        start_index = current_index * self.items_per_page
        end_index = start_index + self.items_per_page
        for i in range(start_index, end_index):
            if i < len(skins):
                skin = skins[i]
                skin_rect = rects[i - start_index]
                if is_color:
                    skin_surface = pygame.Surface((125, 125))
                    skin_surface.fill(skin)
                    self.screen.blit(skin_surface, skin_rect)
                else:
                    self.screen.blit(pygame.transform.scale(skin, skin_rect.size), skin_rect)
                if i == current_skin:
                    pygame.draw.rect(self.screen, self.utils.COLORS['RED'], skin_rect, 4)
        if len(skins) > self.items_per_page:
            left_arrow_rect = pygame.Rect(x - 310, y + 145, 50, 50)  # Ajustez les coordonnées ici
            right_arrow_rect = pygame.Rect(x + 490, y + 145, 50, 50)  # Ajustez les coordonnées ici
            self.screen.blit(self.left_arrow_image, left_arrow_rect)
            self.screen.blit(self.right_arrow_image, right_arrow_rect)
            return left_arrow_rect, right_arrow_rect
        return None, None

    def blit_sound_toggle(self):
        """Affiche le bouton pour activer/désactiver les sons"""
        sound_text = self.font.render(self.utils.custo_sound_on if self.utils.sound_enabled else
                                      self.utils.custo_sound_off, True, self.utils.COLORS['BLACK'])
        sound_rect = sound_text.get_rect(center=(self.utils.WIDTH // 4, self.utils.HEIGHT // 1.5))
        self.screen.blit(sound_text, sound_rect)
        sound_image = self.sound_on_image if self.utils.sound_enabled else self.sound_off_image
        self.screen.blit(sound_image, self.sound_toggle_rect)

    def blit_back_button(self):
        """Affiche le bouton pour retourner au menu principal"""
        back_button_text = self.font.render(self.utils.custo_back, True, self.utils.COLORS['BLACK'])
        self.screen.blit(self.back_image_custo, (self.utils.WIDTH // 2 - 215, self.utils.HEIGHT - 130))
        self.screen.blit(back_button_text, back_button_text.get_rect(center=self.back_button_rect.center))

    def handle_events(self):
        """Gére les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle_mouse_click(event.pos):
                    return True

    def handle_mouse_click(self, pos):
        """Gére le clic de la souris"""
        if self.sound_toggle_rect.collidepoint(pos):
            self.utils.sound_enabled = not self.utils.sound_enabled
            if self.utils.sound_enabled:
                self.utils.load_background_music()
            else:
                self.utils.stop_background_music()
        if self.back_button_rect.collidepoint(pos):
            return True

        if self.left_arrow_archer and self.left_arrow_archer.collidepoint(pos) and self.current_page_archer > 0:
            self.current_page_archer -= 1
        if self.right_arrow_archer and self.right_arrow_archer.collidepoint(pos) and self.current_page_archer < len(
                self.archer_skins) // self.items_per_page:
            self.current_page_archer += 1

        if self.left_arrow_arrow and self.left_arrow_arrow.collidepoint(pos) and self.current_page_arrow > 0:
            self.current_page_arrow -= 1
        if self.right_arrow_arrow and self.right_arrow_arrow.collidepoint(pos) and self.current_page_arrow < len(
                self.arrow_skins) // self.items_per_page:
            self.current_page_arrow += 1

        if self.left_arrow_background and self.left_arrow_background.collidepoint(
                pos) and self.current_page_background > 0:
            self.current_page_background -= 1
        if self.right_arrow_background and self.right_arrow_background.collidepoint(
                pos) and self.current_page_background < len(self.background_colors) // self.items_per_page:
            self.current_page_background += 1

        if self.left_arrow_wall and self.left_arrow_wall.collidepoint(pos) and self.current_page_wall > 0:
            self.current_page_wall -= 1
        if self.right_arrow_wall and self.right_arrow_wall.collidepoint(pos) and self.current_page_wall < len(
                self.wall_skins) // self.items_per_page:
            self.current_page_wall += 1

        if self.left_arrow_lang and self.left_arrow_lang.collidepoint(pos) and self.current_page_lang > 0:
            self.current_page_lang -= 1
        if self.right_arrow_lang and self.right_arrow_lang.collidepoint(pos) and self.current_page_lang < len(
                self.lang_set) // self.items_per_page:
            self.current_page_lang += 1

        self.check_skin_click(pos, self.archer_skin_rects, self.set_archer_skin, self.current_page_archer)
        self.check_skin_click(pos, self.arrow_skin_rects, self.set_arrow_skin, self.current_page_arrow)
        self.check_skin_click(pos, self.background_skin_rects, self.set_background_skin, self.current_page_background)
        self.check_skin_click(pos, self.wall_skin_rects, self.set_wall_skin, self.current_page_wall)
        self.check_skin_click(pos, self.lang_set_rects, self.set_lang_set, self.current_page_lang)
        return False

    def set_archer_skin(self, index):
        """Définie le skin de l'archer"""
        self.current_archer_skin = index
        self.utils.set_archer_skin(index)

    def set_arrow_skin(self, index):
        """Définie le skin de la flèche"""
        self.current_arrow_skin = index
        self.utils.set_arrow_skin(index)

    def set_background_skin(self, index):
        """Définie le skin de fond"""
        self.current_background_skin = index
        self.utils.set_background_skin(index)

    def set_wall_skin(self, index):
        """Définie le skin du mur"""
        self.current_wall_skin = index
        self.utils.set_wall_skin(index)

    def set_lang_set(self, index):
        """Définie le skin de la langue"""
        self.current_lang_set = index
        self.utils.set_lang_set(index)
        self.utils.switch_lang()

    @staticmethod
    def check_skin_click(pos, rects, set_skin_method, current_page):
        """Vérifie si un skin a été cliqué"""
        for i, skin_rect in enumerate(rects):
            if skin_rect.collidepoint(pos):
                set_skin_method(current_page * 5 + i)
