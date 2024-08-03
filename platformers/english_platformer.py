import pickle
from os import path

import pygame

from platformers.platformer_base import (
    Platformer,
    World,
    PlatformerConfig,
    LanguageFx,
    LanguageImages,
    Buttons,
    Button,
    Language,
    Coin,
    LanguageConfig,
)


class EnglishPlatformer(Platformer):
    def __init__(self):
        super().__init__()
        init_level = 0
        if path.exists(f"English/level{init_level}_data"):
            pickle_in = open(f"English/level{init_level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{init_level}_data from file")
        self.world = World(world_data, Language.ENGLISH, self.fx, self.images)

    def reset_world(self, level):
        self.world.player.reset(100, PlatformerConfig.screen_height - 130)
        del self.world

        # load in level data and create world
        if path.exists(f"English/level{level}_data"):
            pickle_in = open(f"English/level{level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{level}_data from file")
        self.world = World(world_data, Language.ENGLISH, self.fx, self.images)

        # create dummy coin for showing the score
        score_coin = Coin(
            PlatformerConfig.tile_size // 2,
            PlatformerConfig.tile_size // 2,
            self.images.coin_img,
        )
        self.world.coin_group.add(score_coin)
        return self.world

    def load_fx(self) -> LanguageFx:
        return LanguageFx(
            pygame.mixer.Sound("English/img/martySpeech.wav"),
            pygame.mixer.Sound("English/img/coin.wav"),
            pygame.mixer.Sound("English/img/jump.wav"),
            pygame.mixer.Sound("English/img/game_over.wav"),
            "English/img/music.wav",
            pygame.mixer.Sound("English/img/optionsound.mp3"),
            pygame.mixer.Sound("English/img/rightans.mp3"),
            pygame.mixer.Sound("English/img/wrongans.wav"),
            "English/img/questionbg.wav",
        )

    def load_images(self) -> LanguageImages:
        return LanguageImages(
            pygame.image.load("English/img/sun.png"),
            pygame.image.load("English/img/bgimg.png"),
            pygame.image.load("English/img/restart_btn.png"),
            pygame.image.load("English/img/start_btn.png"),
            pygame.image.load("English/img/exit_btn.png"),
            pygame.image.load("English/img/martyspeechimg.png"),
            pygame.image.load("English/img/car.png"),
            pygame.image.load("English/img/lava.png"),
            pygame.image.load("English/img/exit.png"),
            pygame.image.load("English/img/platform.png"),
            pygame.image.load(f"English/img/dirt.png"),
            pygame.image.load(f"English/img/grass.png"),
            pygame.image.load(f"English/img/blob.png"),
            pygame.image.load(f"English/img/ghost.png"),
            pygame.image.load("English/img/profslide.png"),
        )

    def load_language_config(self) -> LanguageConfig:
        return LanguageConfig(max_levels=7)

    def load_questions(self) -> (list, list):
        images = [
            "English/img/english/q1.png",
            "English/img/english/q2.png",
            "English/img/english/q3.png",
            "English/img/english/q4.png",
            "English/img/english/q5.png",
            "English/img/english/q6.png",
            "English/img/english/q7.png",
            "English/img/english/q8.png",
            "English/img/english/q9.png",
            "English/img/english/q10.png",
            "English/img/english/q11.png",
            "English/img/english/q12.png",
            "English/img/english/q13.png",
            "English/img/english/q14.png",
            "English/img/english/q15.png",
            "English/img/english/q16.png",
            "English/img/english/q17.png",
            "English/img/english/q18.png",
            "English/img/english/q19.png",
            "English/img/english/q20.png",
        ]
        ansKey = [1, 4, 4, 2, 3, 2, 1, 4, 1, 3, 1, 2, 1, 3, 2, 3, 3, 1, 3, 1]

        return images, ansKey
