import pygame
import random
from pygame.locals import *

# Define the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# This defines the player object
class Player(pygame.sprite.Sprite):
    # Constructor constructs the object
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./assets/jet.png")
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


        # Keeps player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending the pygame Sprite
class Enemy(pygame.sprite.Sprite):
    # Constructor constructs the object
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./assets/missile.png")

        # Random starting position
        self.rect = self.surf.get_rect(
            center = (  
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

        # Random speed
        self.speed = random.randint(5,20)


    # Moves the missiles, removes them when off screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill


# Define the cloud object extending the pygame Sprite
class Cloud(pygame.sprite.Sprite):
    # Constructor constructs the object
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./assets/cloud.png")
        
        # Random starting position
        self.rect = self.surf.get_rect(
            center = (  
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )


    # Move the clouds, remove them when off the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        
    


# Initialized pygame
pygame.init()

# Setup for sounds
pygame.mixer.init()

# Setup the clock
clock = pygame.time.Clock()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and clouds
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) # how often missiles spawn

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create the player
player = Player()

# Create groups to hold our object/sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Loading the background music
pygame.mixer.music.load("./assets/Flight_Music.wav")
pygame.mixer.music.play(loops=-1)

# Load assets
collision_sound = pygame.mixer.Sound("./assets/collision.wav")
explosion = pygame.image.load("./assets/explosion.png")

# Boolean to keep the main loop running
running = True

# Sets score to 0
score = 0

# Main loop
while running:

    # look at every event in the game
    for event in pygame.event.get():

        # Quit if the user closes the window
        if event.type == QUIT:
            pygame.quit()

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies
    enemies.update()

    # Update the position of our clouds
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Checks if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):

        if player.alive():
            collision_sound.play()
            screen.blit(explosion, (player.rect))
        
        
        player.kill()
    

    # Runs for every sprite
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the player's score
    if player.alive():
        score += 1

    # Draw the score
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, [0,0,0])
    screen.blit(text, (0,0))

    # Update the screen
    pygame.display.flip()

    clock.tick(60)
