import pygame
from fighter import Fighter

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawllin - Just a Dev")

bg_image = pygame.image.load("assets/images/background/bg-china.jpg")
scaled_bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_bg():
    screen.blit(scaled_bg_image, (0, 0))
    
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

game_running = True
while game_running:
    draw_bg()
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            
    pygame.display.update()
            
pygame.quit()
