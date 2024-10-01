import json
import os
import pygame


class GameUtils:
    """Classe pour les utilitaires du jeu, contient des méthodes pour charger des images, des sons, des polices, etc."""

    BASE_PATH = "assets"
    COLORS = {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "GREEN": (0, 255, 0),
        "RED": (255, 0, 0),
        "GRAY": (128, 128, 128),
        "BEIGE": (245, 245, 220),
        "LIGHT_YELLOW": (255, 255, 224),
        "LIGHT_BLUE": (173, 216, 230),
        "DARK_BLUE": (0, 0, 128),
        "LIGHT_GREEN": (144, 238, 144),
        "DARK_GREEN": (0, 128, 0),
    }

    def __init__(self):
        pygame.init()
        self.SCREEN_INFO = pygame.display.Info()
        self.WIDTH = int(self.SCREEN_INFO.current_w)
        self.HEIGHT = int(self.SCREEN_INFO.current_h)
        self.archer_skin = 4
        self.arrow_skin = 4
        self.background_skin = 0
        self.wall_skin = 0
        self.lang_set = 0
        self.sound_enabled = True
        self._init_paths()
        self.switch_lang()

    def _init_paths(self):
        """Initialise les chemins des fichiers nécessaires au jeu"""
        self.paths = {
            "background_menu": f"{self.BASE_PATH}/background_menu.png",
            "deco_arrow": f"{self.BASE_PATH}/deco_arrow.png",
            "menu_choice_image": f"{self.BASE_PATH}/pannel_wood.png",
            "menu_panel_exit": f"{self.BASE_PATH}/pannel_exit.png",
            "sound_img_sound_on": f"{self.BASE_PATH}/song_set/song_1.png",
            "sound_img_sound_off": f"{self.BASE_PATH}/song_set/song_2.png",
            "choose_menu_back": f"{self.BASE_PATH}/choose_menu/back.png",
            "choose_menu_start": f"{self.BASE_PATH}/choose_menu/start.png",
            "menu_break_box": f"{self.BASE_PATH}/break_menu/menu_box.png",
            "button_break": f"{self.BASE_PATH}/break_menu/button.png",
            "wall": f"{self.BASE_PATH}/wall/wall.png",
            "victory_trophy": f"{self.BASE_PATH}/victory_screen/trophy.png",
            "info": f"{self.BASE_PATH}/info.png",
            "quit_game": f"{self.BASE_PATH}/quit_game/panel_quit_game.png",
            "left_arrow": f"{self.BASE_PATH}/left_arrow.png",
            "right_arrow": f"{self.BASE_PATH}/right_arrow.png",
            "pause_button": f"{self.BASE_PATH}/break_menu/pause_button.png",
            "font": f"{self.BASE_PATH}/font/PlaywriteIS-VariableFont_wght.ttf",
            "background_music": f"{self.BASE_PATH}/sounds/backgroundMusic.mp3",
            "arrow_sound": f"{self.BASE_PATH}/sounds/shooter.mp3",
            "player_hit_sound": f"{self.BASE_PATH}/sounds/hit.mp3",
            "death_sound": f"{self.BASE_PATH}/sounds/death.mp3",
            "floor_hit_sound": f"{self.BASE_PATH}/sounds/floor_hit.mp3",
            "wall_hit_sound": f"{self.BASE_PATH}/sounds/wall_hit.mp3"
        }

    def load_background_music(self):
        """Charge la musique de fond du jeu"""
        pygame.mixer.music.load(self.paths["background_music"])
        pygame.mixer.music.set_volume(0.09)
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop_background_music():
        """Arrête la musique de fond"""
        pygame.mixer.music.stop()

    @staticmethod
    def load_image(path, size):
        """Charge une image et la redimensionne à la taille spécifiée"""
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    @staticmethod
    def load_font(path, size):
        """Charge une police de caractères avec une taille spécifiée"""
        return pygame.font.Font(path, size)

    @staticmethod
    def load_sound(path):
        """Charge un son"""
        return pygame.mixer.Sound(path)

    def get_base_path(self):
        """Retourne le chemin de base des fichiers du jeu"""
        return self.BASE_PATH

    def get_archer_path(self):
        """Retourne le chemin de l'image de l'archer sélectionné"""
        return f"{self.BASE_PATH}/archer_skin/archer_skin_{self.archer_skin + 1}.png"

    def get_arrow_path(self):
        """Retourne le chemin de l'image de la flèche sélectionnée"""
        return f"{self.BASE_PATH}/arrow_skin/arrow_skin_{self.arrow_skin + 1}.png"

    def get_background_color(self):
        """Retourne la couleur de fond sélectionnée"""
        colors = [self.COLORS["WHITE"], self.COLORS["LIGHT_YELLOW"], self.COLORS["LIGHT_BLUE"], self.COLORS["GRAY"],
                  self.COLORS["BEIGE"], self.COLORS["DARK_BLUE"], self.COLORS["LIGHT_GREEN"], self.COLORS["DARK_GREEN"]]
        return colors[self.background_skin]

    def get_wall_path(self):
        """Retourne le chemin de l'image du mur sélectionné"""
        return f"{self.BASE_PATH}/wall_skin/wall_skin_{self.wall_skin + 1}.png"

    def get_lang_active(self):
        """Retourne la langue active"""
        return self.lang_set + 1

    def set_archer_skin(self, skin):
        """Définit le skin de l'archer"""
        self.archer_skin = skin

    def set_arrow_skin(self, skin):
        """Définit le skin de la flèche"""
        self.arrow_skin = skin

    def set_background_skin(self, skin):
        """Définit le skin de l'arrière-plan"""
        self.background_skin = skin

    def set_wall_skin(self, skin):
        """Définit le skin du mur"""
        self.wall_skin = skin

    def set_lang_set(self, skin):
        """Définit la langue active"""
        self.lang_set = skin

    def switch_lang(self):
        """Définit la langue active et charge les données de langue correspondantes"""
        lang_files = {
            1: "en.json",
            2: "es.json",
            3: "fr.json",
            4: "it.json",
            5: "pt.json",
            6: "de.json",
            7: "pl.json",
            8: "sv.json"
        }
        lang_file = lang_files.get(self.get_lang_active(), "en.json")
        lang_path = os.path.join(self.BASE_PATH, "lang", lang_file)

        with open(lang_path, "r", encoding="utf-8") as file:
            lang_data = json.load(file)
        for key, value in lang_data.items():
            setattr(self, key, value)
