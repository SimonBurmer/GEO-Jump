import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vellocity = vec(0, 0) # player speed 
        self.acceleration = vec(0, 0) # player accelertion

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1 # for checking if player stands on a platform
        hits = pg.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1
        if hits:
            self.vellocity.y = -PLAYER_JUMP
            
    def update(self):
        self.acceleration = vec(0, PLAYER_GRAV)
        # movent
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acceleration.x = -PLAYER_ACC # acceleration left
        if keys[pg.K_d]:
            self.acceleration.x = PLAYER_ACC # accelertion right

        # apply friction
        self.acceleration.x += self.vellocity.x * PLAYER_FRICTION
        # equations of motion
        self.vellocity += self.acceleration
        self.pos += self.vellocity + 0.5 * self.acceleration

        # infinity screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos