import random
import sys
import time
import pygame
import math

from game_mode.vs_computer import VsComputer
from game_mode.vs_player import VsPlayer
from object.archer import Archer
from object.wall import Wall
from object.arrow import Arrow
from game_mode.break_menu import BreakMenu
from object.ia_player import IAPlayer


class Game:
    """ Classe principale du jeu. Gère les éléments du jeu et les interactions entre eux."""

    def __init__(self, screen, running, utils, wind, wall):
        self.screen = screen
        self.running = running
        self.utils = utils
        self.wind = wind
        self.wall = wall

        self.ia_player = IAPlayer(self)  # Instance de l'IA
        self.ai_can_shoot = True
        self.archer1_shoot_ia = False

        self.height_line = int(self.utils.HEIGHT * 0.75)
        self.start_time = pygame.time.get_ticks()  # Temps de début d'une partie de jeu

        self.camera_offset = [0, 0]
        self.camera_target = [0, 0]
        self.clock = pygame.time.Clock()  # Horloge pour gérer les FPS
        self.background_ingame_color = self.utils.get_background_color()

        self.arrow_sound = self.utils.load_sound(self.utils.paths['arrow_sound'])
        self.player_hit_sound = self.utils.load_sound(self.utils.paths['player_hit_sound'])
        self.floor_hit_sound = self.utils.load_sound(self.utils.paths['floor_hit_sound'])
        self.wall_hit_sound = self.utils.load_sound(self.utils.paths['wall_hit_sound'])
        self.font = self.utils.load_font(self.utils.paths['font'], 30)
        self.pause_button = self.utils.load_image(self.utils.paths['pause_button'], (125, 125))

        self.archer1 = Archer(1, self.utils, flipped=False, random=0)
        self.top_rect_1, self.middle_rect_1, self.bottom_rect_1 = self.archer1.get_archer_parts(self.camera_offset, 1)
        self.archer2_x = random.randint(self.utils.WIDTH, self.utils.WIDTH * 2)
        self.archer2 = Archer(2, self.utils, flipped=True, random=int(self.archer2_x))
        self.top_rect_2, self.middle_rect_2, self.bottom_rect_2 = self.archer2.get_archer_parts(self.camera_offset, 2)
        self.turn = 1
        self.camera_offset = [self.utils.WIDTH / 2 - self.archer1.archer_rect_archer1.x, 0]
        self.health1, self.health2 = 100, 100
        self.wind_effect = 0

        self.prev_health1 = self.health1
        self.prev_health2 = self.health2
        self.flash_counter1 = 0
        self.flash_counter2 = 0

        if self.wall:
            wall_width = random.randint(50, 80)
            wall_height = random.randint(200, 620)
            wall_x = (
                             self.archer1.archerRect.x + self.archer1.width + self.archer2.archerRect.x
                             - self.archer2.width) // 2 - wall_width // 6
            wall_y = self.height_line - wall_height - 4
            self.wall = Wall(wall_x, wall_y + 5, wall_width, wall_height, self.utils) if wall else None

        self.arrow = None
        self.on_sound_arrow = True
        self.drawing = False

        self.last_click_time = 0

        self.friendly_fire = False
        self.archer1_friendly_rect = pygame.Rect(self.archer1.archer_rect_archer1.x,
                                                 self.archer1.archer_rect_archer1.y - 50,
                                                 self.archer1.archer_rect_archer1.width, 50)
        self.archer2_friendly_rect = pygame.Rect(self.archer2.archer_rect_archer2.x,
                                                 self.archer2.archer_rect_archer2.y - 50,
                                                 self.archer2.archer_rect_archer2.width, 50)

    def load_sounds(self):
        """" Charge les sons du jeu"""
        self.arrow_sound = self.utils.load_sound(self.utils.paths['arrow_sound'])
        self.player_hit_sound = self.utils.load_sound(self.utils.paths['player_hit_sound'])
        self.floor_hit_sound = self.utils.load_sound(self.utils.paths['floor_hit_sound'])
        self.wall_hit_sound = self.utils.load_sound(self.utils.paths['wall_hit_sound'])

    def handle_events(self):
        """ Gère les événements du jeu."""
        global start_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break_menu = BreakMenu(self, self.utils)
                    break_menu.display()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.last_click_time = time.time()
                mouse_pos = pygame.mouse.get_pos()
                if self.pause_button.get_rect(topleft=(self.utils.WIDTH // 2 - 10, 45)).collidepoint(mouse_pos):
                    break_menu = BreakMenu(self, self.utils)
                    break_menu.display()
                elif self.arrow is None and not self.drawing:
                    start_pos = pygame.mouse.get_pos()
                    if self.wind:
                        self.wind_effect = random.uniform(-0.3, 1)  # Recalcule wind_effect à chaque tour
                    if self.turn == 1:  # Archer 1
                        self.arrow = Arrow(self.archer1.emp_x_1 + 200 + self.camera_offset[0], self.archer1.emp_y_all +
                                           60 + self.camera_offset[1], 100, 50, 10 * (1 + self.wind_effect),
                                           self.utils)
                        self.drawing = True
                    else:  # Archer 2
                        self.arrow = Arrow(self.archer2.random - 30 + self.camera_offset[0], self.archer2.emp_y_all +
                                           60 + self.camera_offset[1], 100, 50,
                                           10 * (1 + self.wind_effect), self.utils)
                        self.drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                click_duration = time.time() - self.last_click_time
                if click_duration < 0.2:  # Pas de tir si le clic est trop court
                    if start_pos is not None:
                        if start_pos == pygame.mouse.get_pos():
                            self.drawing = False
                            self.arrow = None
                            self.on_sound_arrow = True
                            return
                self.drawing = False
                if self.arrow:
                    self.play_song_fly_arrow()
                    self.arrow.calculate_velocity(self.camera_offset)
                    self.arrow.multi_damage -= 0.8
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing and self.arrow:
                    self.arrow.end_pos = pygame.mouse.get_pos()

    @staticmethod
    def lerp(start, end, t):
        """Fonction pour interpoler linéairement entre deux valeurs. """
        return start + t * (end - start)

    def change_turn(self):
        """ Fonction pour changer de tour entre les archers"""
        self.turn = 1 if self.turn % 2 == 0 else 2
        target_x = self.utils.WIDTH / 2 - (
            self.archer1.archer_rect_archer1.x if self.turn == 1 else self.archer2.archer_rect_archer2.x)
        self.camera_target = [target_x, 0]

    def draw_line_and_arrow(self):
        """ Dessine la ligne de visée et la flèche sur l'écran."""
        if self.arrow and self.arrow.start_pos and self.arrow.end_pos:
            distance = min(int(math.hypot(self.arrow.end_pos[0] - self.arrow.start_pos[0],
                                          self.arrow.start_pos[1] - self.arrow.end_pos[1])),
                           self.arrow.MAX_FORCE)
            if distance > 0:
                start_x = self.arrow.start_pos[0]
                start_y = self.arrow.start_pos[1]

                angle = math.atan2(self.arrow.start_pos[1] - self.arrow.end_pos[1],
                                   self.arrow.end_pos[0] - self.arrow.start_pos[0]) + math.pi
                end_x = self.arrow.start_pos[0] + distance * math.cos(angle)
                end_y = self.arrow.start_pos[1] - distance * math.sin(angle)
                pygame.draw.line(self.screen, self.utils.COLORS['BLACK'], (start_x, start_y), (end_x, end_y), 7)

                # Crée un triangle pour indiquer la direction de la flèche
                offset = 10
                triangle_points = [
                    (end_x + offset * math.cos(angle), end_y - offset * math.sin(angle)),
                    (end_x - 20 * math.cos(angle + math.pi / 6), end_y + 20 * math.sin(angle + math.pi / 6)),
                    (end_x - 20 * math.cos(angle - math.pi / 6), end_y + 20 * math.sin(angle - math.pi / 6))
                ]
                pygame.draw.polygon(self.screen, self.utils.COLORS['BLACK'], triangle_points)

                display_angle = int(math.degrees(angle)) % 360

                if display_angle > 180:
                    display_angle -= 360
                font = self.utils.load_font(self.utils.paths['font'], 20)
                text = font.render(f"{self.utils.force} : {distance}, {self.utils.angle} : {display_angle}°",
                                   True, self.utils.COLORS['BLACK'])
                self.screen.blit(text, (
                    start_x + 10,
                    start_y - 30 if start_y > 20 else start_y + 10))

    def draw(self):
        """ Dessine les éléments du jeu"""
        self.screen.fill(self.background_ingame_color)

        self.top_rect_1, self.middle_rect_1, self.bottom_rect_1 = self.archer1.get_archer_parts(self.camera_offset, 1)
        self.top_rect_2, self.middle_rect_2, self.bottom_rect_2 = self.archer2.get_archer_parts(self.camera_offset, 2)

        # Dessine les archers et le mur
        self.archer1.display_archer(self.screen, self.camera_offset, 1)
        self.archer2.display_archer(self.screen, self.camera_offset, 2)
        if self.wall:
            self.wall.display_wall(self.screen, self.camera_offset)

        self.draw_line_and_arrow()

        # Dessine la ligne de séparation entre le sol et les archers
        pygame.draw.line(self.screen, self.utils.COLORS['BLACK'], (0, self.height_line + self.camera_offset[1]),
                         (self.utils.WIDTH, self.height_line + self.camera_offset[1]), 5)

        # Dessine le bouton de pause
        self.screen.blit(self.pause_button, (self.utils.WIDTH // 2 - 25 , 80))

        self.draw_score()  # Dessine le score des joueurs

        self.draw_timer()  # Dessine le timer

        self.draw_arrow()  # Dessine la flèche sur l'écran

    def draw_score(self):
        """ Dessine le score des joueurs sur l'écran"""
        health_color1 = self.utils.COLORS['RED'] if self.flash_counter1 > 0 else self.utils.COLORS['BLACK']
        health_color2 = self.utils.COLORS['RED'] if self.flash_counter2 > 0 else self.utils.COLORS['BLACK']
        if self.flash_counter1 == 1:
            self.flash_counter1 -= 1
        if self.flash_counter2 == 1:
            self.flash_counter2 -= 1
        if self.health1 <= 0:
            self.health1 = 0
        if self.health2 <= 0:
            self.health2 = 0
        health_text1 = self.font.render(f"{self.utils.healthP1} : {self.health1:.2f}", True, health_color1)
        health_text2 = self.font.render(f"{self.utils.healthP2} : {self.health2:.2f}", True, health_color2)
        turn_text = self.font.render(self.utils.game_turn + f" {self.turn}", True, self.utils.COLORS['BLACK'])
        self.screen.blit(health_text1, (10, 10))
        self.screen.blit(health_text2, (self.utils.WIDTH - 320, 10))
        self.screen.blit(turn_text, (self.utils.WIDTH // 2 - 80, 10))

    def draw_timer(self):
        """ Dessine le timer sur l'écran"""
        elapsed_time = self.get_elapsed_time()
        time_text = self.font.render(self.utils.elapsed_time + elapsed_time, True, self.utils.COLORS['BLACK'])
        self.screen.blit(time_text, (self.utils.WIDTH // 2 - 100, 50))

    def get_elapsed_time(self):
        """Calcule le temps écoulé depuis le début du jeu."""
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        elapsed_seconds = elapsed_time_ms // 1000
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def draw_arrow(self):
        """ Dessine la flèche sur l'écran."""
        if self.arrow and self.arrow.circle_pos:
            rotation_angle = math.degrees(math.atan2(-self.arrow.velocity[1], self.arrow.velocity[0]))
            rotated_image = pygame.transform.rotate(self.arrow.image, rotation_angle)
            rect = rotated_image.get_rect(center=(int(self.arrow.circle_pos[0] + self.camera_offset[0]),
                                                  int(self.arrow.circle_pos[1] + self.camera_offset[1])))
            self.screen.blit(rotated_image, rect.topleft)
            self.camera_offset[0] = self.utils.WIDTH / 2. - self.arrow.circle_pos[0]
            self.camera_offset[1] = self.utils.HEIGHT / 2 - self.arrow.circle_pos[1]
            self.arrow.circle_pos[0] += self.arrow.velocity[0]
            self.arrow.circle_pos[1] += self.arrow.velocity[1]
            self.arrow.velocity[1] += self.arrow.GRAVITY

    def update_camera(self):
        """ Met à jour la position de la caméra"""
        self.camera_offset[0] = self.lerp(self.camera_offset[0], self.camera_target[0], 0.1)
        self.camera_offset[1] = self.lerp(self.camera_offset[1], self.camera_target[1], 0.1)

    def update(self):
        """ Met à jour les éléments du jeu"""
        self.update_camera()
        if not self.arrow:
            return
        if self.arrow.circle_pos and self.arrow.circle_pos[1] >= self.height_line:  # Collision avec le sol
            self.play_song_floor()
            self.restart_arrow_function()
            return

        if self.arrow and self.arrow.circle_pos:
            arrow_rect = pygame.Rect(self.arrow.circle_pos[0] + self.camera_offset[0],
                                     self.arrow.circle_pos[1] + self.camera_offset[1], 15, 15)

            # Collision avec les archers pour le tir ami
            if (self.turn == 1 and arrow_rect.colliderect(self.archer1_friendly_rect.move(self.camera_offset))) or \
                    (self.turn == 2 and arrow_rect.colliderect(self.archer2_friendly_rect.move(self.camera_offset))):
                self.friendly_fire = True

            # Collision avec le mur
            if self.wall and arrow_rect.colliderect(self.wall.get_wall_rect(self.camera_offset)):
                self.play_song_wall()
                self.restart_arrow_function()
                return
            # Collision avec les archers
            if self.turn == 1 or self.friendly_fire:
                if arrow_rect.colliderect(self.top_rect_2):
                    self._handle_hit(2, 50)
                elif arrow_rect.colliderect(self.middle_rect_2):
                    self._handle_hit(2, 20)
                elif arrow_rect.colliderect(self.bottom_rect_2):
                    self._handle_hit(2, 10)
            if self.turn == 2 or self.friendly_fire:
                if arrow_rect.colliderect(self.top_rect_1):
                    self._handle_hit(1, 50)
                elif arrow_rect.colliderect(self.middle_rect_1):
                    self._handle_hit(1, 20)
                elif arrow_rect.colliderect(self.bottom_rect_1):
                    self._handle_hit(1, 10)

    def _handle_hit(self, id_archer, damage):
        """ Fonction pour gérer les dégâts infligés à un archer et changer de tour"""
        if self.utils.sound_enabled:
            self.player_hit_sound.play()
        if id_archer == 1:
            self.flash_counter1 += 1
            self.health1 -= damage * abs(self.arrow.multi_damage) / 10
            self.archer1_shoot_ia = True
        elif id_archer == 2:
            self.flash_counter2 += 1
            self.health2 -= damage * abs(self.arrow.multi_damage) / 10
        self.restart_arrow_function()
        if self.friendly_fire:
            self.alert_friendly_fire()

    def alert_friendly_fire(self):
        """ Fonction pour alerter l'utilisateur d'un tir ami avec animation"""
        text = self.font.render(self.utils.friendly_fire_alert, True, self.utils.COLORS['RED'])
        text_rect = text.get_rect(center=(self.utils.WIDTH // 2, self.utils.HEIGHT // 2))
        start_y = text_rect.y
        end_y = start_y - 150
        alpha = 255

        for y in range(start_y, end_y, -2):
            self.draw()
            text.set_alpha(alpha)
            self.screen.blit(text, (text_rect.x, y))
            pygame.display.update()
            alpha -= 5
            if alpha < 0:
                alpha = 0
            pygame.time.delay(40)

        self.friendly_fire = False

    def restart_arrow_function(self):
        """ Fonction pour redémarrer la flèche"""
        self.change_turn()
        self.arrow = None
        self.drawing = False
        self.on_sound_arrow = True
        self.ai_can_shoot = True

    def play_song_floor(self):
        """ Fonction pour jouer le son de la flèche qui touche le sol"""
        if self.utils.sound_enabled:
            self.floor_hit_sound.play()

    def play_song_fly_arrow(self):
        """ Fonction pour jouer le son de la flèche qui vole"""
        if self.utils.sound_enabled and self.on_sound_arrow:
            self.arrow_sound.play()
            self.on_sound_arrow = False

    def play_song_wall(self):
        """ Fonction pour jouer le son de la flèche qui touche le mur"""
        if self.utils.sound_enabled:
            self.wall_hit_sound.play()

    def run_game_vs_player(self):
        """ Lance le jeu en mode joueur contre joueur"""
        vs_player = VsPlayer(self, self.utils, self.wind, self.wall)
        vs_player.run()

    def run_game_vs_computer(self):
        """ Lance le jeu en mode joueur contre ordinateur"""
        vs_computer = VsComputer(self, self.utils, self.wind, self.wall)
        vs_computer.run()

    def ia_shoot(self):
        """ Fonction pour gérer le tir de l'IA"""
        self.ia_player.ia_shoot()

    def get_archer1_shoot(self):
        """ Vérifie si l'archer 1 a été touché par la flèche"""
        shoot = self.archer1_shoot_ia
        self.archer1_shoot_ia = False
        return shoot

    def clean_screen(self):
        """ Nettoie l'écran du jeu"""
        self.screen.fill(self.background_ingame_color)
        pygame.display.update()
