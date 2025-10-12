import pygame
from random import randint , uniform
from os.path import join 

class Player(pygame.sprite.Sprite):
    
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("Space shooter", "space 2 surfaces", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_rect(center = (w/2,h/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        
        #laser time and cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.laser_cooldown_duration = 400
        
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.laser_shoot_time >= self.laser_cooldown_duration:
                self.can_shoot = True
        
        
        
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - (keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - (keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        if keys[pygame.K_SPACE] and self.can_shoot:
            laser(laser_surf, self.rect.midtop, (all_sprites , laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

class star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (randint(0,w), randint(0,h)))

class laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom = pos)
    
    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.duplicate = surf
        self.image = self.duplicate
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        self.rotation_speed = randint(40,80)
        self.rotation = 0 
    
    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.duplicate ,self.rotation , 1)
        self.rect = self.image.get_rect(center = self.rect.center)
        
        if self.rect.centery > h:
            self.kill()

class animation(pygame.sprite.Sprite):
    def  __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(center = pos)
    def update(self,dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collisions():
    global  running 
    
    collision = pygame.sprite.spritecollide(player , meteor_sprites , True, pygame.sprite.collide_mask)
    
    if collision:
        running = False 
    
    for laser in laser_sprites:
        collide = pygame.sprite.spritecollide(laser , meteor_sprites , True)
        
        if collide:
            laser.kill()
            explosion_sound.play()
            animation(animation_frames ,laser.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True , (240,240,240))
    text_rect = text_surf.get_rect(midbottom = (w /2 , h - 50))
    screen.blit(text_surf , text_rect)
    pygame.draw.rect(screen , (240,240,240) , text_rect.inflate(20,15).move(0,-3), 8,12 )

#initializing
pygame.init()
w = 1280
h = 720      

clock = pygame.time.Clock()

screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Space Shooter")
running = True

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#importing
star_surface = pygame.image.load(join("Space shooter", "space 2 surfaces", "images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("Space shooter", "space 2 surfaces", "images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(join("Space shooter", "space 2 surfaces", "images", "meteor.png")).convert_alpha()
font = pygame.font.Font(join("Space shooter", "space 2 surfaces", "images", "Oxanium-Bold.ttf"),40)
animation_frames = [pygame.image.load(join("Space shooter", "space 2 surfaces", "images", "explosion", f"{i}.png")).convert_alpha()  for i in range(21)]

laser_sound = pygame.mixer.Sound(join("Space shooter", "space 2 surfaces", "audio", "laser.wav"))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join("Space shooter", "space 2 surfaces", "audio", "explosion.wav"))
game_music = pygame.mixer.Sound(join("Space shooter", "space 2 surfaces", "audio", "game_music.wav"))
game_music.set_volume(0.4)
game_music.play(loops = -1)


for i in range (20):
    star(all_sprites, star_surface)
player = Player(all_sprites)



#custom events

meteor_event = pygame.time.get_ticks()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x,y = randint(0,w), randint(-200,-100)
            meteor(meteor_surface,(x,y),(all_sprites, meteor_sprites))
            
        
    collisions()
    
    all_sprites.update(dt)
    
    screen.fill('#3a2e3f')
    all_sprites.draw(screen)
    display_score()
    pygame.display.update()
    
pygame.quit()