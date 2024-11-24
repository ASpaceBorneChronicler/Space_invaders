import pygame
import os
import random
from pygame.locals import *

# Initialize Pygame and create window
pygame.init()
clock = pygame.time.Clock()
FPS = 80

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
FONT_40 = pygame.font.SysFont('Arial', 40)
ROWS = 5
COLS = 5
PLAYER_SPEED = 5
BULLET_SPEED = 5
ALIEN_BULLET_SPEED = 2
ALIEN_MOVE_DISTANCE = 1
ALIEN_MOVE_THRESHOLD = 50
BULLET_COOLDOWN = 500
ALIEN_BULLET_COOLDOWN = 1000
MAX_ALIEN_BULLETS = 5

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load and scale images once
def load_image(name):
    return pygame.image.load(os.path.join('img', name))

# Cache all images
IMAGES = {
    'background': pygame.transform.scale(load_image('bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    'player': load_image('spaceship.png'),
    'alien': load_image('alien.png'),
    'bullet': load_image('bullet.png'),
    'alien_bullet': load_image('alien_bullet.png'),
    'explosion': [load_image(f'exp{i}.png') for i in range(1, 6)]
}

# Pre-scale explosion images
EXPLOSION_SIZES = {
    1: [(pygame.transform.scale(img, (20, 20))) for img in IMAGES['explosion']],
    2: [(pygame.transform.scale(img, (40, 40))) for img in IMAGES['explosion']],
    3: [(pygame.transform.scale(img, (60, 60))) for img in IMAGES['explosion']]
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize a new Player instance.

        :param x: The x-coordinate for the center of the player
        :param y: The y-coordinate for the center of the player
        :return: None
        """
        super().__init__()
        self.image = IMAGES['player']
        self.rect = self.image.get_rect(center=(x, y))
        self.last_shot = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.health_start = 3
        self.health_remaining = 3

    def update(self):
        keys = pygame.key.get_pressed()


        # Vertical movement
        if keys[pygame.K_UP] and self.rect.top > 500:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED
        
        # Horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

        # Shooting
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.last_shot > BULLET_COOLDOWN:
            bullet_group.add(Bullets(self.rect.centerx, self.rect.top))
            self.last_shot = current_time
        
        # GEtting hit
        if pygame.sprite.spritecollide(self, invader_bullet_group, True, pygame.sprite.collide_mask):
            self.health_remaining -= 1
        red = (255, 0, 0)
        green = (0, 255, 0)
        #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosions(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
        # return -1

class Invaders(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize a new Invaders instance.

        :param x: The x-coordinate for the center of the invader
        :param y: The y-coordinate for the center of the invader
        :return: None
        """
        super().__init__()
        self.image = IMAGES['alien']
        self.rect = self.image.get_rect(center=(x, y))
        self.move_direction = 1
        self.move_counter = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.move_direction * ALIEN_MOVE_DISTANCE
        self.move_counter += 1
        if abs(self.move_counter) > ALIEN_MOVE_THRESHOLD:
            self.move_direction *= -1
            self.move_counter *= -1

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES['bullet']
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
        
        # Use sprite collision with mask
        for invader in pygame.sprite.spritecollide(self, invader_group, True, pygame.sprite.collide_mask):
            self.kill()
            explosion_group.add(Explosions(invader.rect.centerx, invader.rect.centery, 2))
            break

class Invader_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES['alien_bullet']
        self.rect = self.image.get_rect(center=(x, y+5))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += ALIEN_BULLET_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Explosions(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        """
        Initialize a new Explosions instance.

        :param x: The x-coordinate for the center of the explosion
        :param y: The y-coordinate for the center of the explosion
        :param size: The size of the explosion (1, 2, or 3)
        :return: None
        """
        super().__init__()
        self.images = EXPLOSION_SIZES[size]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0
        self.explosion_speed = 3

    def update(self):
        self.counter += 1
        if self.counter % self.explosion_speed == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]

def generate_invaders():
    """
    Generate a grid of invaders with the specified number of rows and columns.

    This function will add each invader to the invader_group.

    :return: None
    """

    for row in range(ROWS):
        for col in range(COLS):
            invader_group.add(Invaders(80 + col * 100, 70 + row * 70))

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Sprite Groups
bullet_group = pygame.sprite.Group()
invader_group = pygame.sprite.Group()
invader_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()

# Create player and invaders
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
spaceship_group.add(player)
generate_invaders()


# Game loop
last_alien_bullet = pygame.time.get_ticks()
running = True
game_over = 0
countdown = 3
last_count = pygame.time.get_ticks()


while running:
    # Time management
    clock.tick(FPS)

    # Draw background first
    screen.blit(IMAGES['background'], (0, 0))


    if countdown == 0:

        # Alien shooting logic
        time_now = pygame.time.get_ticks()
        if (time_now - last_alien_bullet > ALIEN_BULLET_COOLDOWN and 
            len(invader_group) > 0 and 
            len(invader_bullet_group) <= MAX_ALIEN_BULLETS):
            shooting_alien = random.choice(invader_group.sprites())
            invader_bullet_group.add(Invader_Bullets(shooting_alien.rect.centerx, shooting_alien.rect.bottom))
            last_alien_bullet = time_now

        # Check win/lose conditions
        if len(invader_group) == 0:
            game_over = 1
        elif player.health_remaining <= 0:
            game_over = -1

        if game_over == 0: # Checks if game is not over
            # Update sprites
            for group in (spaceship_group, bullet_group, invader_group, 
                        invader_bullet_group, explosion_group):
                group.update()
        
        elif game_over == -1: # Checks if game is lost
            explosion_group.draw(screen)
            explosion_group.update()
            draw_text(screen, 'GAME OVER!', FONT_40, (255, 0, 0), 
                     int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2))
            
        else:   # Checks if game is won
            draw_text(screen, 'YOU WIN!', FONT_40, (0, 255, 0), 
                     int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2))
            
    # Game countdown
    if countdown > 0:
        draw_text(screen, 'GET READY!', FONT_40, (225,225,225), int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 50))
        draw_text(screen, str(countdown),FONT_40, (225,225,225), int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    # Draw sprites
    for group in (spaceship_group, bullet_group, invader_group, 
                invader_bullet_group, explosion_group):
        group.draw(screen)    

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()

pygame.quit()