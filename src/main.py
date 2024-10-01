import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from utils import GameUtils
from screen.menu import Menu


class Main:
    """Classe principale du jeu. Appelée au lancement du jeu."""
    def __init__(self):
        pygame.init()

        # Initialisation des utilitaires du jeu
        self.utils = GameUtils()

        # Dimensions de la fenêtre du jeu
        self.SCREEN = pygame.display.set_mode((self.utils.WIDTH, self.utils.HEIGHT), pygame.NOFRAME)

        # Chargement de la musique de fond
        self.utils.load_background_music()

        # État du jeu
        self.running = True


if __name__ == "__main__":
    main = Main()
    menu = Menu(main.SCREEN, main.running, main.utils)
    menu.show_menu()
