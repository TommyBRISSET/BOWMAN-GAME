import random
import pygame
from game_mode.victory_screen import VictoryScreen


class VsComputer:
    """Classe qui gère le mode de jeu contre l'ordinateur"""
    def __init__(self, game, utils, wind, wall):
        self.game = game
        self.utils = utils
        self.wind = wind
        self.wall = wall

        self.ai_shoot_time = pygame.time.get_ticks() + random.randint(4000, 6000)
        self.player_death_sound = self.utils.load_sound(self.utils.paths['death_sound'])
        self.ai_shoot_delay = 0

    def run(self):
        """Fonction qui gère le déroulement du jeu contre l'ordinateur"""
        while self.game.running:
            self.handle_game_loop()

    def handle_game_loop(self):
        """Gérer la boucle principale du jeu"""
        self.game.handle_events()
        self.handle_ai_shooting()
        self.game.update()
        self.game.draw()
        pygame.display.update()
        self.game.clock.tick(60)
        self.check_victory()

    def handle_ai_shooting(self):
        """Gérer le tir de l'IA"""
        current_time = pygame.time.get_ticks()
        if self.game.turn == 2 and self.game.ai_can_shoot:
            if self.ai_shoot_delay == 0:
                self.ai_shoot_delay = current_time + random.randint(1000, 2000)
            elif current_time >= self.ai_shoot_delay:
                self.game.ai_can_shoot = False
                self.game.arrow_sound.play()
                self.game.ia_shoot()
                self.ai_shoot_delay = 0
                self.ai_shoot_time = current_time + random.randint(5000, 7000)

    def check_victory(self):
        """Vérifier si un joueur a gagné"""
        if self.game.health1 <= 0 or self.game.health2 <= 0:
            if self.utils.sound_enabled:
                self.player_death_sound.play()
            winner = self.utils.player1 if self.game.health2 <= 0 else self.utils.player2
            victory_screen = VictoryScreen(self.game.screen, self.utils, self.game.get_elapsed_time())
            action = victory_screen.display(winner, self.game.running)
            if action == 'replay':
                self.reset_game()
                self.run()

    def reset_game(self):
        """Réinitialiser le jeu"""
        self.game.clean_screen()
        self.game.__init__(self.game.screen, self.game.running, self.utils, self.wind, self.wall)
        self.ai_shoot_time = pygame.time.get_ticks() + random.randint(4000, 6000)
