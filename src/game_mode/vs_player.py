import pygame
from game_mode.victory_screen import VictoryScreen


class VsPlayer:
    """Classe qui gère le mode de jeu Joueur contre Joueur"""
    def __init__(self, game, utils, wind, wall):
        self.game = game
        self.utils = utils
        self.wind = wind
        self.wall = wall

        self.player_death_sound = self.utils.load_sound(self.utils.paths['death_sound'])

    def run(self):
        """Fonction qui gère le déroulement du jeu Joueur contre Joueur"""
        while self.game.running:
            self.handle_game_loop()

    def handle_game_loop(self):
        """Gérer la boucle principale du jeu"""
        self.game.handle_events()
        self.game.update()
        self.game.draw()
        pygame.display.update()
        self.game.clock.tick(60)
        self.check_victory()

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
