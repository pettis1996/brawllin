import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawllin - Just a Dev")

bg_image = pygame.image.load("assets/background/bg-china.jpg")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_bg():
    screen.blit(bg_image, (0, 0))

game_running = True
while game_running:
    draw_bg()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            
    pygame.display.update()
            
pygame.quit()
