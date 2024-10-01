import pygame
import math


class Arrow:
    def __init__(self, posx, posy, width, height, multidamage, utils):
        self.start_pos = [posx, posy]
        self.end_pos = self.start_pos
        self.velocity = [0, 0]
        self.GRAVITY = 0.05
        self.MAX_FORCE = 100
        self.SPEED_DIVISOR = 6
        self.width = width
        self.height = height
        self.multi_damage = multidamage
        self.utils = utils

        # Charger l'image de la flèche
        self.image = pygame.transform.scale(
            pygame.image.load(self.utils.get_arrow_path()), (self.width, self.height))

        self.arrowRect = self.image.get_rect()
        self.arrowRect.x, self.arrowRect.y = posx, posy
        self.circle_pos = None

    def calculate_velocity(self, camera_offset):
        """Calcule la vélocité de la flèche en fonction de la force et de l'angle de tir"""
        if self.start_pos != self.end_pos:
            force = min(int(math.hypot(self.end_pos[0] - self.start_pos[0], self.start_pos[1] - self.end_pos[1])),
                        self.MAX_FORCE) / self.SPEED_DIVISOR
            angle = math.atan2(self.start_pos[1] - self.end_pos[1], self.end_pos[0] - self.start_pos[0]) + math.pi
            self.velocity = [force * math.cos(angle), -force * math.sin(angle)]
            self.circle_pos = [self.start_pos[0] + force * self.SPEED_DIVISOR * math.cos(angle) - camera_offset[0],
                               self.start_pos[1]
                               - force * self.SPEED_DIVISOR * math.sin(angle) - camera_offset[1]]
            self.start_pos = None
            self.end_pos = None
