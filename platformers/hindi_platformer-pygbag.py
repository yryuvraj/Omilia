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


class HindiPlatformer(Platformer):
    def __init__(self):
        super().__init__()
        init_level = 0
        if path.exists(f"hindi/level{init_level}_data"):
            pickle_in = open(f"hindi/level{init_level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{init_level}_data from file")
        self.world = World(world_data, Language.HINDI, self.fx, self.images)

    def reset_world(self, level):
        self.world.player.reset(100, PlatformerConfig.screen_height - 130)
        del self.world

        # load in level data and create world
        if path.exists(f"hindi/level{level}_data"):
            pickle_in = open(f"hindi/level{level}_data", "rb")
            world_data = pickle.load(pickle_in)
        else:
            raise Exception(f"Could not load level{level}_data from file")
        self.world = World(world_data, Language.HINDI, self.fx, self.images)

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
            pygame.mixer.Sound("hindi/img/martySpeech.ogg"),
            pygame.mixer.Sound("hindi/img/coin.ogg"),
            pygame.mixer.Sound("hindi/img/jump.ogg"),
            pygame.mixer.Sound("hindi/img/game_over.ogg"),
            "hindi/img/music.ogg",
            pygame.mixer.Sound("hindi/img/optionsound.ogg"),
            pygame.mixer.Sound("hindi/img/rightans.ogg"),
            pygame.mixer.Sound("hindi/img/wrongans.ogg"),
            "hindi/img/questionbg.ogg",
        )

    def load_images(self) -> LanguageImages:
        return LanguageImages(
            pygame.image.load("hindi/img/sun.png"),
            pygame.image.load("hindi/img/bgimg.png"),
            pygame.image.load("hindi/img/restart_btn.png"),
            pygame.image.load("hindi/img/start_btn.png"),
            pygame.image.load("hindi/img/exit_btn.png"),
            pygame.image.load("hindi/img/martyspeechimg.png"),
            pygame.image.load("hindi/img/car.png"),
            pygame.image.load("hindi/img/lava.png"),
            pygame.image.load("hindi/img/exit.png"),
            pygame.image.load("hindi/img/platform.png"),
            pygame.image.load(f"hindi/img/dirt.png"),
            pygame.image.load(f"hindi/img/grass.png"),
            pygame.image.load(f"hindi/img/blob.png"),
            pygame.image.load(f"hindi/img/ghost.png"),
            pygame.image.load("hindi/img/profslide.png"),
        )

    def load_language_config(self) -> LanguageConfig:
        return LanguageConfig(max_levels=7)

    def load_questions(self) -> (list, list):
        images = [
            "hindi/img/hindiImg/q1h.png",
            "hindi/img/hindiImg/q2h.png",
            "hindi/img/hindiImg/q3h.png",
            "hindi/img/hindiImg/q4h.png",
            "hindi/img/hindiImg/q5h.png",
            "hindi/img/hindiImg/q6h.png",
            "hindi/img/hindiImg/q7h.png",
            "hindi/img/hindiImg/q8h.png",
            "hindi/img/hindiImg/q9h.png",
            "hindi/img/hindiImg/q10h.png",
            "hindi/img/hindiImg/q11h.png",
            "hindi/img/hindiImg/q12h.png",
            "hindi/img/hindiImg/q13h.png",
            "hindi/img/hindiImg/q14h.png",
            "hindi/img/hindiImg/q15h.png",
            "hindi/img/hindiImg/q16h.png",
            "hindi/img/hindiImg/q17h.png",
            "hindi/img/hindiImg/q18h.png",
            "hindi/img/hindiImg/q19h.png",
            "hindi/img/hindiImg/q20h.png",
        ]
        ansKey = [1, 4, 4, 2, 3, 2, 1, 4, 1, 3, 1, 2, 1, 3, 2, 3, 3, 1, 3, 1]

        return images, ansKey
