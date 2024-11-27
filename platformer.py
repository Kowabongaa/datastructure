import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario-like Platformer")

clock = pygame.time.Clock()
FPS = 60

# Load Images
player_img = pygame.image.load("player.png").convert_alpha()
background_img = pygame.image.load("/mnt/data/background.png").convert_alpha()
background_width = background_img.get_width()
background_img = pygame.transform.scale(background_img, (background_width, SCREEN_HEIGHT))

# Collision Areas - Manually defined for different sections in the background
collision_rects = [
    pygame.Rect(0, 560, 400, 40),    # Ground section 1
    pygame.Rect(420, 560, 800, 40),  # Ground section 2
    pygame.Rect(860, 440, 80, 120),  # Pipe 1
    pygame.Rect(1300, 520, 80, 80),  # Stairs part 1
    pygame.Rect(1380, 480, 80, 120), # Stairs part 2
    pygame.Rect(1460, 440, 80, 160), # Stairs part 3
    pygame.Rect(1540, 400, 80, 200)  # Stairs part 4
]

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 5
        self.jump_speed = -15
        self.gravity = 1
        self.y_velocity = 0
        self.on_ground = False

    def update(self, keys, collision_rects):
        # Horizontal Movement
        if keys[K_LEFT]:
            self.rect.x -= self.velocity
        if keys[K_RIGHT]:
            self.rect.x += self.velocity

        # Apply Gravity
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # Check Collision with Defined Areas
        self.on_ground = False
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if self.y_velocity > 0:  # Falling Down
                    self.rect.bottom = rect.top
                    self.y_velocity = 0
                    self.on_ground = True

        # Jumping
        if keys[K_SPACE] and self.on_ground:
            self.y_velocity = self.jump_speed

# Main Game Loop
def main_game():
    player = Player(100, 500)
    running = True
    camera_x = 0

    while running:
        # Scroll background with player
        camera_x = player.rect.x - SCREEN_WIDTH // 2
        if camera_x < 0:
            camera_x = 0
        elif camera_x > background_width - SCREEN_WIDTH:
            camera_x = background_width - SCREEN_WIDTH

        # Draw scrolling background
        screen.blit(background_img, (-camera_x, 0))

        # Get Key Presses
        keys = pygame.key.get_pressed()
        player.update(keys, collision_rects)

        # Draw Player
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        # Debug: Draw Collision Rectangles
        for rect in collision_rects:
            adjusted_rect = pygame.Rect(rect.x - camera_x, rect.y, rect.width, rect.height)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_rect, 2)  # Red outline for debugging

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Update Screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Start the main game
main_game()
