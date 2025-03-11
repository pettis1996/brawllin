import pygame
from fighter import Fighter

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawllin - Just a Dev")

clock = pygame.time.Clock()
FPS = 60

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

bg_image = pygame.image.load("assets/images/background/bg-china.jpg")
scaled_bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_bg():
    screen.blit(scaled_bg_image, (0, 0))
    
def draw_health_bar(health, x, y):
    ratio = health / 100
    
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

game_running = True
while game_running:
    clock.tick(FPS)
    
    draw_bg()
    
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            
    pygame.display.update()
            
pygame.quit()
