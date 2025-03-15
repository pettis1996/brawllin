import pygame

class Fighter:
    def __init__(self, player, x, y, data, sprite_sheet, animation_steps):
        self.player = player # 1: Player 1, 2: Player 2
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False # Flip to face same direction
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self.frame_index = 0 # Used for animating the images to move on the list of animations
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) # Player hit box
        self.vel_y = 0 # Velocity on Y axis for jump
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack1_cooldown = 0
        self.attack2_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        
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
        
    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        
        dx = 0
        dy = 0
        
        self.running = False
        self.attack_type = 0
        
        key = pygame.key.get_pressed()
        
        # Cannot perform movement when attacking
        if not self.attacking and self.alive and not round_over:
            # Movement on X axis
            
            # Player 1 Movement
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                    
                # Movement on Y axis - Jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                    
                # Attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
                    self.attack(target)
        
            if self.player == 2:
                    if key[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = SPEED
                        self.running = True
                        
                    # Movement on Y axis - Jump
                    if key[pygame.K_UP] and not self.jump:
                        self.vel_y = -30
                        self.jump = True
                        
                    # Attack
                    if key[pygame.K_o] or key[pygame.K_p]:
                        if key[pygame.K_o]:
                            self.attack_type = 1
                        if key[pygame.K_p]:
                            self.attack_type = 2
                        self.attack(target)
        
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
        if target.rect.centerx > self.rect.centerx and self.alive:
            self.flip = False
        else:
            self.flip = True
        
        # Apply attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1
        
        self.rect.x += dx
        self.rect.y += dy
    
    # Animation updates
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) # Player dead
        elif self.hit:
            self.update_action(5) # Player got hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3) # Player attacks with attack 1
            elif self.attack_type == 2:
                self.update_action(4) # Player attacks with attack 2
        elif self.jump:
            self.update_action(2) # Player jumps
        elif self.running:
            self.update_action(1) # Player moves
        else: 
            self.update_action(0) # Player is idle
        
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            
            # Check if an attack was executed
            if self.action == 3 or self.action == 4:
                self.attacking = False
                if self.action == 3:
                    self.attack1_cooldown = 20
                elif self.action == 4:
                    self.attack2_cooldown = 40
            
            # Check if player is hit
            if self.action == 5:
                self.hit = False
                self.attacking = False
                self.attack1_cooldown = 20
                self.attack2_cooldown = 40
    
    def attack(self, target):
        # Different attack cooldown
        if (self.attack_type == 1 and self.attack1_cooldown == 0) or (self.attack_type == 2 and self.attack2_cooldown == 0):
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                if self.attack_type == 1:
                    target.health -= 10
                    self.attack1_cooldown = 20  
                elif self.attack_type == 2:
                    target.health -= 20
                    self.attack2_cooldown = 40  
                target.hit = True

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action  
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))