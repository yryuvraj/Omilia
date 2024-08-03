import random
import sys
from dataclasses import dataclass
from platformers.assets.enums import *
from platformers.assets.configs import *
from platformers.assets.sprites import *
from platformers.assets.data import *

import pygame
from pygame import mixer

from GameEnding import endscreen


class World:
    def __init__(self, world_data, language: Language, fx: LanguageFx, images: LanguageImages):
        self.coin_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.blob_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.tile_list = []
        self.world_data = world_data
        self.images = images
        self.fx = fx
        self.player = Player(100, PlatformerConfig.screen_height - 130, language, self.images, self.fx)
        pygame.mixer.music.load(self.fx.bg_music_path)
        pygame.mixer.music.play(-1)
        row_count = 0
        tile_size = PlatformerConfig.tile_size
        for row in world_data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(self.images.dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(self.images.grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(
                        col_count * tile_size,
                        row_count * tile_size + 15,
                        self.images.enemy_img,
                    )
                    self.blob_group.add(blob)
                if tile == 4:
                    platform = Platform(
                        col_count * tile_size,
                        row_count * tile_size,
                        1,
                        0,
                        self.images.platform,
                    )
                    self.platform_group.add(platform)
                if tile == 5:
                    platform = Platform(
                        col_count * tile_size,
                        row_count * tile_size,
                        0,
                        1,
                        self.images.platform,
                    )
                    self.platform_group.add(platform)
                if tile == 6:
                    lava = Lava(
                        col_count * tile_size,
                        row_count * tile_size + (tile_size // 2),
                        self.images.lava_img,
                    )
                    self.lava_group.add(lava)
                if tile == 7:
                    coin = Coin(
                        col_count * tile_size + (tile_size // 2),
                        row_count * tile_size + (tile_size // 2),
                        self.images.coin_img,
                    )
                    self.coin_group.add(coin)
                if tile == 8:
                    exit_tile = Exit(
                        col_count * tile_size,
                        row_count * tile_size - (tile_size // 2),
                        self.images.exit,
                    )
                    self.exit_group.add(exit_tile)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        screen.blit(self.images.sun_img, (100, 100))
        screen.blit(self.images.bg_img, (0, 0))
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        screen.blit(self.player.image, self.player.rect)
        self.platform_group.draw(screen)
        self.blob_group.draw(screen)
        self.coin_group.draw(screen)
        self.lava_group.draw(screen)
        self.exit_group.draw(screen)

    def handle_collisions(self) -> CollisionType:
        player = self.player

        # check for collision with enemies
        if pygame.sprite.spritecollide(player, self.blob_group, False):
            return CollisionType.BLOB

        # check for collision with lava
        if pygame.sprite.spritecollide(player, self.lava_group, False):
            return CollisionType.LAVA

        # check for collision with exit
        if pygame.sprite.spritecollide(player, self.exit_group, False):
            return CollisionType.EXIT

        # check for collision with boundary
        for tile in self.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(player.rect.x + player.dx, player.rect.y, player.width, player.height):
                player.dx = 0
            # check for collision in y direction
            if tile[1].colliderect(player.rect.x, player.rect.y + player.dy, player.width, player.height):
                # check if below the ground i.e. jumping
                if player.vel_y < 0:
                    player.dy = tile[1].bottom - player.rect.top
                    player.vel_y = 0
                # check if above the ground i.e. falling
                elif player.vel_y >= 0:
                    player.dy = tile[1].top - player.rect.bottom
                    player.vel_y = 0
                    player.in_air = False

        # check for collision with platforms
        for platform in self.platform_group:
            # collision in the x direction
            if platform.rect.colliderect(player.rect.x + player.dx, player.rect.y, player.width, player.height):
                player.dx = 0
            # collision in the y direction
            if platform.rect.colliderect(player.rect.x, player.rect.y + player.dy, player.width, player.height):
                # check if below platform
                if abs((player.rect.top + player.dy) - platform.rect.bottom) < player.col_thresh:
                    player.vel_y = 0
                    player.dy = platform.rect.bottom - player.rect.top
                # check if above platform
                elif abs((player.rect.bottom + player.dy) - platform.rect.top) < player.col_thresh:
                    player.rect.bottom = platform.rect.top - 1
                    player.in_air = False
                    player.dy = 0
                # move sideways with the platform
                if platform.move_x != 0:
                    player.rect.x += platform.move_direction

        # update player coordinates
        player.rect.x += player.dx
        player.rect.y += player.dy
        if pygame.sprite.spritecollide(player, self.coin_group, True):
            return CollisionType.COIN
        return CollisionType.NONFATAL


class Platformer:
    """Interface for different platformer languages. SHOULD NOT BE INSTANTIATED DIRECTLY"""

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pygame.init()
        pygame.display.set_caption("Omilia")
        # define game variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (PlatformerConfig.screen_width, PlatformerConfig.screen_height),
            pygame.RESIZABLE,
        )
        self.level_state: LevelState = LevelState.START
        self.world: World | None = None
        self.fx = self.load_fx()
        self.images = self.load_images()
        self.buttons = self.create_buttons()
        self.platformer_state = PlatformerState.MAIN_MENU
        self.questions, self.answers = self.load_questions()
        self.score = 0
        self.language_config = self.load_language_config()
        self.first_pass = True

    def draw_text(self, text, font, text_colour, x, y):
        img = font.render(text, True, text_colour)
        self.screen.blit(img, (x, y))

    def load_language_config(self) -> LanguageConfig:
        pass

    def reset_world(self, level) -> World:
        pass

    def load_fx(self) -> LanguageFx:
        pass

    def load_images(self) -> LanguageImages:
        pass

    def create_buttons(self) -> Buttons:
        return Buttons(
            start_button=Button(
                PlatformerConfig.screen_width // 2 - 350,
                PlatformerConfig.screen_height // 2,
                self.images.start_img,
            ),
            restart_button=Button(
                PlatformerConfig.screen_width // 2 - 50,
                PlatformerConfig.screen_height // 2 + 100,
                self.images.restart_img,
            ),
            exit_button=Button(
                PlatformerConfig.screen_width // 2 + 150,
                PlatformerConfig.screen_height // 2,
                self.images.exit_img,
            ),
        )

    def load_questions(self) -> (list, list):
        pass

    def run(self):
        run_window = True
        current_level = 0
        while run_window:
            self.clock.tick(PlatformerConfig.fps)

            # if self.platformer_state == PlatformerState.MAIN_MENU:
            #     if self.buttons.exit_button.draw(self.screen):
            #         run_window = False
            #     if self.buttons.start_button.draw(self.screen):
            #         self.platformer_state = PlatformerState.PLAYING_LEVEL
            if self.platformer_state == PlatformerState.MAIN_MENU:
                self.fx.martyspeech_fx.play()
                self.platformer_state = PlatformerState.PLAYING_LEVEL

            if self.platformer_state == PlatformerState.QUIT:
                pygame.quit()

            if self.platformer_state == PlatformerState.PLAYING_LEVEL:
                self.platformer_state = self.play_level(current_level)

            if self.platformer_state == PlatformerState.QUESTION:
                question_state = self.play_question(current_level, first=self.first_pass)
                match question_state:
                    case QuestionState.CORRECT:
                        current_level += 1
                        if current_level > self.language_config.max_levels:
                            self.platformer_state = PlatformerState.WON
                        else:
                            self.platformer_state = PlatformerState.PLAYING_LEVEL
                    case QuestionState.INCORRECT:
                        self.score = 0
                        self.handle_death()
                        self.world = self.reset_world(current_level)
                        self.platformer_state = PlatformerState.PLAYING_LEVEL

            if self.platformer_state == PlatformerState.WON:
                self.draw_text(
                    "YOU WIN!",
                    PlatformerConfig.font,
                    Colours.BLUE.value,
                    (PlatformerConfig.screen_width // 2) - 140,
                    PlatformerConfig.screen_height // 2,
                )
                endscreen()
                # if self.buttons.restart_button.draw(self.screen):
                #     self.platformer_state = PlatformerState.PLAYING_LEVEL
                #     current_level = 0
                #     self.score = 0

    def play_level(self, level):
        self.world = self.reset_world(level)
        level_time = 0
        self.level_state = LevelState.PLAYING
        platformer_state = PlatformerState.PLAYING_LEVEL
        while self.level_state == LevelState.PLAYING:
            self.clock.tick(PlatformerConfig.fps)
            level_time += 1
            pygame.display.update()
            self.world.draw(self.screen)
            self.draw_text(
                "X " + str(self.score),
                PlatformerConfig.font_score,
                Colours.WHITE.value,
                PlatformerConfig.tile_size - 10,
                10,
            )
            if self.first_pass and level_time < PlatformerConfig.martyimg_time:
                self.screen.blit(self.images.martyspeech_img, (0, 0))
            self.world.blob_group.update()
            self.world.platform_group.update()
            level_time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            self.handle_keypress()
            collision = self.world.handle_collisions()
            match collision:
                case CollisionType.BLOB:
                    self.fx.game_over_fx.play()
                    self.handle_death()
                    self.level_state = LevelState.PLAYING
                    self.world = self.reset_world(level)
                    self.score = 0
                case CollisionType.LAVA:
                    self.fx.game_over_fx.play()
                    self.handle_death()
                    self.level_state = LevelState.PLAYING
                    self.world = self.reset_world(level)
                    self.score = 0
                case CollisionType.EXIT:
                    self.level_state = LevelState.EXIT
                    platformer_state = PlatformerState.QUESTION
                case CollisionType.COIN:
                    self.fx.coin_fx.play()
                    self.score += 1
                case CollisionType.NONFATAL:
                    pass

        return platformer_state

    def handle_death(self):
        restart_clicked = False
        while not restart_clicked:
            self.draw_text(
                "GAME OVER!",
                PlatformerConfig.font,
                Colours.BLUE.value,
                (PlatformerConfig.screen_width // 2) - 200,
                PlatformerConfig.screen_height // 2,
            )
            self.world.player.animate_ghost()
            self.clock.tick(PlatformerConfig.fps)
            pygame.display.update()
            self.world.draw(self.screen)
            self.draw_text(
                "X " + str(self.score),
                PlatformerConfig.font_score,
                Colours.WHITE.value,
                PlatformerConfig.tile_size - 10,
                10,
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level_state = LevelState.GAME_OVER
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            restart_clicked = self.buttons.restart_button.draw(self.screen)

    def play_question(self, level, first=False) -> QuestionState:
        pygame.mixer.music.load(self.fx.question_bg_music)
        pygame.mixer.music.play(-1)
        self.screen.fill((255, 255, 255))
        if first:
            textfont = pygame.font.Font("bangla/img/CompassPro.ttf", 32)
            text = """Marty, Try to guess what the word!"""
            self.first_pass = False
            self.screen.blit(self.images.prof_slide, (0, 0))
            proftext = textfont.render(text, True, (255, 255, 255))
            self.screen.blit(proftext, (550, 600))
            pygame.display.update()
            prof_read = False
            while not prof_read:
                self.clock.tick(PlatformerConfig.fps)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        prof_read = True

        n = random.randint(0, len(self.questions) - 1)
        question_image = pygame.image.load(f"{self.questions[n]}")
        self.screen.blit(question_image, (0, 0))

        # wait for click
        option_selected = None
        buttons = [
            pygame.Rect(100, 255, 290, 300),
            pygame.Rect(610, 255, 290, 300),
            pygame.Rect(100, 625, 290, 300),
            pygame.Rect(610, 635, 290, 300),
        ]

        while not option_selected:
            pygame.display.update()
            mx, my = pygame.mouse.get_pos()

            def select_button():
                for i, button in enumerate(buttons):
                    if button.collidepoint((mx, my)):
                        self.fx.option_sound.play()
                        return i + 1
                return None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    option_selected = select_button()

        if option_selected == self.answers[n]:
            self.fx.correct_sound.play()
            return QuestionState.CORRECT
        else:
            self.fx.wrong_sound.play()
            return QuestionState.INCORRECT

    def handle_keypress(self):
        self.world.player.reset_movement()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.world.player.can_jump():
            self.fx.jump_fx.play()
            self.world.player.jump()
        if not keys[pygame.K_SPACE]:
            self.world.player.jumped = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.world.player.left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.world.player.right()
        if (keys[pygame.K_LEFT] is False or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] is False or keys[pygame.K_d]):
            self.world.player.reset_counter()
        self.world.player.animate()
