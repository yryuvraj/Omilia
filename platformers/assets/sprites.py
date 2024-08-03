import pygame
from platformers.assets.enums import Language
from platformers.assets.configs import PlatformerConfig


class Player:
    def __init__(self, x, y, langauge: Language, language_images, language_fx):
        self.language = langauge
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"{self.language.value}/img/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.dx = 0
        self.walk_cooldown = 5
        self.col_thresh = 20
        self.dy = 0
        self.images = language_images
        self.fx = language_fx

    def animate_ghost(self):
        self.image = self.images.dead_img
        if self.rect.y > 200:
            self.rect.y -= 5

    def reset(self, x, y):
        self.__init__(x, y, self.language, self.images, self.fx)

    def reset_movement(self):
        self.dx = 0
        self.dy = 0

    def reset_counter(self):
        self.counter = 0
        self.index = 0
        if self.direction == 1:
            self.image = self.images_right[self.index]
        if self.direction == -1:
            self.image = self.images_left[self.index]

    def can_jump(self):
        return not self.jumped and not self.in_air

    def jump(self):
        if self.can_jump():
            self.vel_y = -15
            self.jumped = True

    def left(self):
        self.dx -= 5
        self.counter += 1
        self.direction = -1

    def right(self):
        self.dx += 5
        self.counter += 1
        self.direction = 1

    def animate(self):
        if self.counter > self.walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy += self.vel_y
        self.in_air = True


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button
        screen.blit(self.image, self.rect)
        return action


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (PlatformerConfig.tile_size, PlatformerConfig.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (PlatformerConfig.tile_size, int(PlatformerConfig.tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (PlatformerConfig.tile_size // 2, PlatformerConfig.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (PlatformerConfig.tile_size, PlatformerConfig.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
