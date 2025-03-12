import pygame

class Fighter:
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        
    def load_images(self, sprite_sheet, animation_steps):
        # Extract images from Sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
        
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        
        dx = 0
        dy = 0
        
        key = pygame.key.get_pressed()
        
        # Cannot perform movement when attacking
        if not self.attacking:
            # Movement on X axis
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
                
            # Movement on Y axis - Jump
            if key[pygame.K_w] and not self.jump:
                self.vel_y = -30
                self.jump = True
                
            # Attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2
        
        self.vel_y += GRAVITY
        dy += self.vel_y
         
        # Avoid edges X and Y   
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        
        # The side that the players are facing
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        self.rect.x += dx
        self.rect.y += dy
    
    # Animation updates
    def update(self):
        animation_cooldown = 500
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
    
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
       
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))