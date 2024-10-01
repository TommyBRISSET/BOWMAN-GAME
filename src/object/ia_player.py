import random
import math
import time
import pygame
from object.arrow import Arrow


class IAPlayer:
    """Classe pour gérer le joueur IA"""
    def __init__(self, game):
        self.game = game
        self.previous_shots = []
        self.min_angle = -math.pi / 4
        self.max_angle = math.pi / 4
        self.min_force = 50
        self.max_force = 100

    def ia_shoot(self):
        """Fonction pour gérer le tir de l'IA"""
        start_pos = self.get_start_position()
        shooting_angle, force = self.calculate_shot_parameters(start_pos)
        self.shoot_arrow(start_pos, shooting_angle, force)

    def get_start_position(self):
        """Renvoie la position de départ de l'IA"""
        return self.game.archer2.random - 20, self.game.archer2.emp_y_all + 65

    def calculate_shot_parameters(self, start_pos):
        """Calculer les paramètres du tir"""
        if self.previous_shots:
            last_shot = self.previous_shots[-1]
            if last_shot['hit']:
                return round(last_shot['angle'], 3), round(last_shot['force'], 1)
            if last_shot['too_far']:
                self.max_force = last_shot['force'] - 10
            else:
                self.min_force = last_shot['force'] + 10
            if last_shot['behind']:
                self.min_angle = last_shot['angle'] + 0.1
            else:
                self.max_angle = last_shot['angle'] - 0.1

        shooting_angle = round(random.uniform(self.min_angle, self.max_angle), 3)
        force = round(random.uniform(self.min_force, self.max_force), 1)
        return shooting_angle, force

    def shoot_arrow(self, start_pos, shooting_angle, force):
        """Fonction pour tirer une flèche"""
        end_pos = (
            start_pos[0] + force * math.cos(shooting_angle) + self.game.camera_offset[0],
            start_pos[1] + force * math.sin(shooting_angle) + self.game.camera_offset[1]
        )

        self.game.arrow = Arrow(self.game.archer2.random - 20 + self.game.camera_offset[0],
                                self.game.archer2.emp_y_all + 65 + self.game.camera_offset[1], 100, 50,
                                10, self.game.utils)
        self.game.arrow.end_pos = end_pos

        for i in range(int(force)):
            self.game.draw()
            self.game.draw_line_and_arrow()
            pygame.display.update()
            time.sleep(0.02)

        self.game.arrow.calculate_velocity(self.game.camera_offset)
        hit, too_far, behind = self.check_hit(end_pos)
        self.previous_shots.append({'target_x': end_pos[0], 'hit': hit,
                                    'too_far': too_far, 'behind': behind, 'angle': shooting_angle, 'force': force})

    def check_hit(self, end_pos):
        """Fonction pour vérifier si la flèche a touché la cible"""
        hit = self.game.get_archer1_shoot()
        too_far = end_pos[0] > self.game.archer2.random - 20
        behind = end_pos[0] < self.game.archer2.random - 20

        return hit, too_far, behind
