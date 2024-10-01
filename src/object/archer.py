import pygame


class Archer:
    """Classe représentant les archers du jeu"""

    # noinspection PyUnresolvedReferences
    def __init__(self, player_id, utils, flipped=False, random=None):
        """Initialisation de l'archer"""
        self.player_id = player_id
        self.utils = utils
        self.flipped = flipped  # True si l'archer est retourné, False sinon
        self.random = int(random)

        self.emp_y_all = int(self.utils.HEIGHT * 0.75) - 200
        self.archerRect = None
        self.archer = None
        self.top_rect = None
        self.middle_rect = None
        self.bottom_rect = None

        if self.player_id == 1:  # Parametre joueur 1
            self.width = 180
            self.height = 200
            self.x = 100
            self.emp_x_1 = int(self.utils.WIDTH // 5)
            self.load_archer()
            self.archer_rect_archer1 = self.archer.get_rect(topleft=(self.emp_x_1, self.emp_y_all))

        else:  # Parametre joueur 2
            self.width = 180
            self.height = 200
            self.x = self.random
            self.load_archer()
            self.archer_rect_archer2 = self.archer.get_rect(topleft=(self.random, self.emp_y_all))

    def load_archer(self):
        """Charge l'image de l'archer"""
        self.archer = pygame.transform.scale(
            pygame.image.load(self.utils.get_archer_path()), (self.width, self.height))
        if self.flipped:
            self.archer = pygame.transform.flip(self.archer, True, False)

        self.archerRect = self.archer.get_rect()
        self.archerRect.x, self.archerRect.y = int(self.x), int(self.emp_y_all)

    def display_archer(self, screen, camera_offset, id_player):
        """Affiche l'archer sur l'écran"""
        if id_player == 1:
            screen.blit(self.archer, (self.archer_rect_archer1[0] + camera_offset[0], self.archer_rect_archer1[1]
                                      + camera_offset[1]))
        elif id_player == 2:
            screen.blit(self.archer, (self.archer_rect_archer2[0] + camera_offset[0], self.archer_rect_archer2[1]
                                      + camera_offset[1]))

    def calculate_rects(self, x, y, camera_offset):
        """Calcule les rectangles représentant les parties supérieure, médiane et inférieure de l'archer"""
        top_rect = pygame.Rect(x + camera_offset[0], y + camera_offset[1], self.archerRect.w, self.archerRect.h // 3)
        middle_rect = pygame.Rect(x + camera_offset[0], y + self.archerRect.h // 3 + camera_offset[1],
                                  self.archerRect.w, self.archerRect.h // 3)
        bottom_rect = pygame.Rect(x + camera_offset[0], y + 2 * self.archerRect.h // 3 + camera_offset[1],
                                  self.archerRect.w, self.archerRect.h // 3)
        return top_rect, middle_rect, bottom_rect

    def get_archer_parts(self, camera_offset, id_player):
        """Retourne les rectangles représentant les parties supérieure, médiane et inférieure de l'archer"""
        if id_player == 1:
            x = self.emp_x_1
        else:
            x = self.random
        y = self.emp_y_all
        return self.calculate_rects(x, y, camera_offset)
