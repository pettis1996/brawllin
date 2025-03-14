import pygame
from fighter import Fighter

pygame.init()

# Window Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Setting up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawllin - Just a Dev")

clock = pygame.time.Clock()
FPS = 60

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game Variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
fight_text_count = 50
last_fight_text_count = pygame.time.get_ticks()
score = [0, 0] # [P1, P2]
round_over = False
ROUND_OVER_COUNTDOWN = 2000 # ms
current_round = 1

# Warrior Variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

# Wizard Variables
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load the background
bg_image = pygame.image.load("assets/images/background/bg-china.jpg").convert_alpha()
scaled_bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sheets with all animations
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Fonts
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

"""
    text: String -> Text to draw
    font: Pygame Font -> Text Font
    text_col: Tuple | string -> Text Color
    x: Integer -> Coordinates on X axis
    y: Integer -> Coordinates on Y axis
"""
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to draw the background image
def draw_bg():
    screen.blit(scaled_bg_image, (0, 0))
    
"""
    health: Integer -> Fighter's health
    x: Integer -> Coordinates on X axis
    y: Integer -> Coordinates on Y axis
"""
def draw_health_bar(health, x, y):
    ratio = health / 100
    
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    
fighter_1 = Fighter(1, 200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 310, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

# True if the game is running
game_running = True
while game_running:
    # Set FPS cap
    clock.tick(FPS)
    
    # Draw the background
    draw_bg()
    
    # Draw Player Health Bars
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    
    # Draw Player Scores
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 925, 60)
    
    # Draw Round Count
    draw_text("ROUND", score_font, RED, 465, 10)
    draw_text(f"{current_round}", score_font, RED, 497, 40)
    
    # If countdown at the beginning is over
    if intro_count <= 0:
        # Show the "FIGHT" text on screen
        if fight_text_count >= 0:
            if (pygame.time.get_ticks() - last_fight_text_count) >= 1:
                fight_text_count -= 1
                last_fight_text_count = pygame.time.get_ticks()
                draw_text("FIGHT", count_font, RED, SCREEN_WIDTH / 3 + 80, SCREEN_HEIGHT / 3)
                
        # Call move() on both players
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    
    fighter_1.update()
    fighter_2.update()
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    # Handle game rounds
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        draw_text("VICTORY", count_font, RED, SCREEN_WIDTH / 3 + 40, SCREEN_HEIGHT / 3)
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COUNTDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
            fighter_2 = Fighter(2, 700, 310, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
            current_round += 1
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stop the loop and end the game
            game_running = False
            
    pygame.display.update()
            
pygame.quit()