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


class BanglaPlatformer(Platformer):
    def __init__(self):
        super().__init__()
        init_level = 0
        if path.exists(f"bangla/level{init_level}_data"):
            pickle_in = open(f"bangla/level{init_level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{init_level}_data from file")
        self.world = World(world_data, Language.BANGLA, self.fx, self.images)
        # pygame.mixer.music.play(-1)

    def reset_world(self, level):
        self.world.player.reset(100, PlatformerConfig.screen_height - 130)
        del self.world

        # load in level data and create world
        if path.exists(f"bangla/level{level}_data"):
            pickle_in = open(f"bangla/level{level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{level}_data from file")
        self.world = World(world_data, Language.BANGLA, self.fx, self.images)

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
            pygame.mixer.Sound("bangla/img/martySpeech.ogg"),
            pygame.mixer.Sound("bangla/img/coin.ogg"),
            pygame.mixer.Sound("bangla/img/jump.ogg"),
            pygame.mixer.Sound("bangla/img/game_over.ogg"),
            "bangla/img/music.ogg",
            pygame.mixer.Sound("bangla/img/optionsound.ogg"),
            pygame.mixer.Sound("bangla/img/rightans.ogg"),
            pygame.mixer.Sound("bangla/img/wrongans.ogg"),
            "bangla/img/questionbg.ogg",
        )

    def load_images(self) -> LanguageImages:
        return LanguageImages(
            pygame.image.load("bangla/img/sun.png"),
            pygame.image.load("bangla/img/bgimg.png"),
            pygame.image.load("bangla/img/restart_btn.png"),
            pygame.image.load("bangla/img/start_btn.png"),
            pygame.image.load("bangla/img/exit_btn.png"),
            pygame.image.load("bangla/img/martyspeechimg.png"),
            pygame.image.load("bangla/img/car.png"),
            pygame.image.load("bangla/img/lava.png"),
            pygame.image.load("bangla/img/exit.png"),
            pygame.image.load("bangla/img/platform.png"),
            pygame.image.load(f"bangla/img/dirt.png"),
            pygame.image.load(f"bangla/img/grass.png"),
            pygame.image.load(f"bangla/img/blob.png"),
            pygame.image.load(f"bangla/img/ghost.png"),
            pygame.image.load("bangla/img/profslide.png"),
        )

    def load_language_config(self) -> LanguageConfig:
        return LanguageConfig(max_levels=7)

    def load_questions(self) -> (list, list):
        images = [
            "bangla/img/banglaimg/q1b.png",
            "bangla/img/banglaimg/q2b.png",
            "bangla/img/banglaimg/q3b.png",
            "bangla/img/banglaimg/q4b.png",
            "bangla/img/banglaimg/q5b.png",
            "bangla/img/banglaimg/q6b.png",
            "bangla/img/banglaimg/q7b.png",
            "bangla/img/banglaimg/q8b.png",
            "bangla/img/banglaimg/q9b.png",
            "bangla/img/banglaimg/q10b.png",
            "bangla/img/banglaimg/q11b.png",
            "bangla/img/banglaimg/q12b.png",
            "bangla/img/banglaimg/q13b.png",
            "bangla/img/banglaimg/q14b.png",
            "bangla/img/banglaimg/q15b.png",
            "bangla/img/banglaimg/q16b.png",
            "bangla/img/banglaimg/q17b.png",
            "bangla/img/banglaimg/q18b.png",
            "bangla/img/banglaimg/q19b.png",
            "bangla/img/banglaimg/q20b.png",
        ]
        ansKey = [1, 4, 4, 2, 3, 2, 1, 4, 1, 3, 1, 2, 1, 3, 2, 3, 3, 1, 3, 1]

        return images, ansKey
