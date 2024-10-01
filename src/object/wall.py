import pygame


class Wall:
    """Classe représentant un mur dans le jeu"""
    def __init__(self, x, y, width, height, utils):
        self.utils = utils
        self.rect = pygame.Rect(x, y, width, height)
        self.wall_image = utils.load_image(self.utils.get_wall_path(), (width, height))
        self.wall_x = int(x)
        self.wall_y = int(y)
        self.wall_rect = self.wall_image.get_rect(topleft=(self.wall_x, self.wall_y))

    def get_wall_rect(self, camera_offset):
        """Retourne le rectangle du mur ajusté avec l'offset de la caméra"""
        return self.wall_rect.move(camera_offset[0], camera_offset[1])

    def display_wall(self, screen, camera_offset):
        """Afficher le mur sur l'écran"""
        screen.blit(self.wall_image, (self.wall_rect[0] + camera_offset[0], self.wall_rect[1] + camera_offset[1]))
