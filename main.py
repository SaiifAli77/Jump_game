import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.index = 0
        self.jump = pygame.image.load("graphics/player/jump.png")
        self.walk = [player_walk_1, player_walk_2]
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.sound = pygame.mixer.Sound("audio/jump.mp3")
        self.sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk): self.index = 0
            self.image = self.walk[int(self.index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle (pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= 2 : self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    else: return True
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("runner")
clock = pygame.time.Clock()
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
start_font = pygame.font.Font("font/Pixeltype.ttf", 80)
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.2)
bg_music.play(loops= -1)
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

def display_score() :
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = game_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center  = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

start_time = 0
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

start_text_surf = start_font.render("Press To Play", False, (64, 64, 64))
start_text_rect = start_text_surf.get_rect(center = (400, 200))
# obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_timer = pygame.USEREVENT +  2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)
# game status
game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(["fly", "snail", "snail"])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()

        game_active = collision_sprite()
    else:
        screen.blit(start_text_surf, start_text_rect)


    pygame.display.update()
    clock.tick(60)