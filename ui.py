import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)

    """
        text: String -> Text to draw
        font: Pygame Font -> Text Font
        text_col: Tuple | string -> Text Color
        x: Integer -> Coordinates on X axis
        y: Integer -> Coordinates on Y axis
    """
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))


    # Function to draw the background image
    def draw_bg(self, scaled_bg_image):
        self.screen.blit(scaled_bg_image, (0, 0))


    """
        Draw the player's health bar
        health: Integer -> Fighter's health
        x: Integer -> Coordinates on X axis
        y: Integer -> Coordinates on Y axis
    """
    def draw_health_bar(self, health, x, y):
        ratio = health / 100

        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    """
        Draw player's action bar
        attack_image: Pygame Image -> The skill image for the attack
        attack_button: String -> The button used for the attack
        x: Coordinates on X axis
        y: Coordinates on Y axis
    """
    def draw_attack_slot(self, attack_image, attack_button, x, y):
        pygame.draw.rect(self.screen, self.RED, (x, y, 60, 60))
        self.screen.blit(attack_image, (x, y))