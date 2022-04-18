import pygame

import animation


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('sprites/player.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, 16, 8)
        self.old_position = self.position.copy()
        self.speed = 1.5
        self.animation_speed = 10
        self.animation_counter = 0
        self.animation_index = 0
        self.health = 3
        self.max_health = 10
        self.screen = pygame.display.set_mode((800, 600))

    def get_damage(self):
        if self.health > 0:
            self.health -= 1

    def get_health(self):
        if self.health < self.max_health:
            self.health += 1

    def full_hearts(self):
        for heart in range(self.health):
            self.screen.blits(pygame.image.load('coeur.png'), (heart * 50, 45))

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                self.screen.blits(pygame.image.load('coeur.png'), (heart * 50, 45))
            else:
                self.screen.blits(pygame.image.load('0 coeur.png'), (heart * 50, 45))

    def half_hearts(self):
        half_hearts_total = self.health / 2
        half_hearts_exists = half_hearts_total - int(half_hearts_total) != 0   

    def teleport_to(self, x, y):
        self.position = [x, y]
        self.save_location()
        self.update()

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        # sprite et animation
        self.animation_counter += 1
        if self.animation_counter > self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % 3
        self.image = self.get_image(self.animation_index * 32, 64)
        self.image.set_colorkey([0, 0, 0])

    def move_left(self):
        self.position[0] -= self.speed
        # sprite
        self.animation_counter += 1
        if self.animation_counter > self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % 3
        self.image = self.get_image(self.animation_index * 32, 32)
        self.image.set_colorkey([0, 0, 0])

    def move_up(self):
        self.position[1] -= self.speed
        # sprite
        self.animation_counter += 1
        if self.animation_counter > self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % 3
        self.image = self.get_image(self.animation_index * 32, 96)
        self.image.set_colorkey([0, 0, 0])

    def move_down(self):
        self.position[1] += self.speed
        # sprite
        self.animation_counter += 1
        if self.animation_counter > self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % 3
        self.image = self.get_image(self.animation_index * 32, 0)
        self.image.set_colorkey([0, 0, 0])

    def update(self):
        self.rect.topleft = self.position
        self.rect.midbottom = self.rect.midbottom
        self.feet.x = self.position[0] + 8
        self.feet.y = self.position[1] + 24
        print(self.health)
        self.full_hearts()
        self.empty_hearts()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.rect.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    full_heart = pygame.image.load('coeur.png')
    half_hearth = pygame.image.load('demi coeur.png')
    empty_heath = pygame.image.load('0 coeur.png')
