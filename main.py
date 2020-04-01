import pygame 
import random
import os
from player import *
from platforms import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("GEO-Jump")
        self.clock = pygame.time.Clock()
        self.running = True #for programm loop
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = os.path.dirname(__file__)
        with open(os.path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        #start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        #load start platforms
        for plat in START_PLATFORMS:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platform_sprites.add(p)
        
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Update
        self.all_sprites.update()


        # check if player hits a platform, only if falling
        if self.player.vellocity.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platform_sprites, False)
            if hits:  
                if self.player.rect.bottom < hits[0].rect.bottom: #for better collision
                    #put the player ontop of the platform and his vellocity.y = 0
                    self.player.pos.y = hits[0].rect.top 
                    self.player.vellocity.y = 0
                
                if self.player.vellocity.y > 5: #needed by bad performance
                    #put the player ontop of the platform and his vellocity.y = 0
                    self.player.pos.y = hits[0].rect.top 
                    self.player.vellocity.y = 0

        # if player reaches top 1/4 of screen
        # move everything for the amount of the player.vellocity.y down
        if self.player.rect.top <= HEIGHT / 4:
            #you only can reach the top 1/4 of the screen while Jumping
            self.player.pos.y += abs(self.player.vellocity.y) #abs -> |self.player.vellocity.y|
            for plat in self.platform_sprites:
                plat.rect.y += abs(self.player.vellocity.y)
                #kill old platforms and count score
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10


        #ckeck if player dies
        if self.player.rect.bottom > HEIGHT:
            #for a good looking dead
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vellocity.y, 10) #max() compares the two values an takes the highes
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platform_sprites) == 0:
            self.playing = False


        # spawn new platforms to keep same average number
        if self.playing and self.platform_sprites.sprites()[-1].rect.top > 100 and len(self.platform_sprites) < 5:
            #difficulty grades
            if self.score < 150:
                minWidth, maxWidth = 60, 160
            else:
                minWidth, maxWidth = 20, 100

            width = random.randrange(minWidth, maxWidth)
            p = Platform(random.randrange(0, WIDTH - width),
                        random.randrange(-30, -10),
                        width, 10)
            self.platform_sprites.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #check for jumping
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game start screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 5)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 5+50)
        self.draw_text("A/D to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT /2 +30)

        pygame.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 5)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 5+70)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT /2 +30)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 5 + 40)
            with open(os.path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 5 + 40)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(pygame.font.match_font(FONT_NAME), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_end_screen()

pygame.quit()
