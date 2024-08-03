from dataclasses import dataclass
import pygame


@dataclass
class PlatformerConfig:
    screen_width: int = 1000
    screen_height: int = 1000
    fps: int = 60
    tile_size: int = 50
    white: tuple = (255, 255, 255)
    blue: tuple = (0, 0, 255)
    world_data: list = None
    font: pygame.font = pygame.font.SysFont("Bauhaus 93", 70)
    font_score: pygame.font = pygame.font.SysFont("Bauhaus 93", 30)
    martyimg_time: int = 600


@dataclass
class LanguageConfig:
    max_levels: int
