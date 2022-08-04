# shmup
# sound effects by Juhani Junkala
import pygame
import random
from os import path

asset_dir = path.join(path.dirname(__file__), "assets")
img_dir = path.join(asset_dir, "img")
audio_dir = path.join(asset_dir, "audio")

WIDTH = 480
HEIGHT = 600
FPS = 60
  
#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#start pygame and create window
pygame.init() #initializes pygame
pygame.mixer.init() #init mixer (sound & music)
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create screen with set size
pygame.display.set_caption("Shmup") #game title
clock = pygame.time.Clock() # handles how fast game run

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #boolean true=anti alias
    text_rect = text_surface.get_rect() # to be able to place rectangle
    text_rect.midtop = (x, y) #midtop:x and y at the point midtop of the rectangle
    surf.blit(text_surface, text_rect) #text_rect, to be able to location place 


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK) #makes player bg transparent
        self.rect = self.image.get_rect() #define rect
        self.radius = 21 
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2 #x pos
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed() #get_pressed() knows what keys u pressed
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx= 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH: #doesnt let player go past right walls
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width* .88 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  
        self.rect.x = random.randrange(WIDTH - self.rect.width) #(0,width-rect_width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0 #rotation
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks() #how many tick since game started

    def rotate(self):
        now = pygame.time.get_ticks() #what time is it now
        if now - self.last_update > 50: #now vs last time updated
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 #keeps from number getting bigger
            new_image = pygame.transform.rotate(self.image_orig, self.rot) 
            #improve rotating animation
            old_center = self.rect.center
            self.image = new_image #updates the rectange
            self.rect = self.image.get_rect() #new rectangle
            self.rect.center = old_center # put it in same center as old one

    def update(self):
        self.rotate()
        self.rect.y += self.speedy #moves the rock vertically
        self.rect.x += self.speedx #moves the rock horizontally
        if self.rect.top> HEIGHT or self.rect.left < -130 or self.rect.right > WIDTH + 130:
            self.rect.x = random.randrange(WIDTH - self.rect.width) #(0,width-rectwidth)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (4, 37))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy #remove when bullet moves off the screen
        if self.rect.bottom < 0:
            self.kill() #remove sprite

#load all game graphics
background = pygame.image.load(path.join(img_dir, "spacebg.png")).convert()
background_rect = background.get_rect() #make it place it so we have a place to locate it
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
#meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laserBlue01.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_med1.png",
               "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small2.png",
               "meteorBrown_tiny1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(audio_dir, "laser.wav"))
expl_sound = []
for sounds in ['expl1.wav', 'expl2.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(audio_dir, sounds)))

pygame.mixer.music.load(path.join(audio_dir, 'bgmusic.ogg'))
pygame.mixer.music.set_volume(0.8)

all_sprites = pygame.sprite.Group() #collection of sprite
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8): #spawns mob
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0

pygame.mixer.music.play(loops=-1) #-1 tells it to go back to start
#game loop
running = True
while running:
    clock.tick(FPS) #game running speed

    # Process input (events) section
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #checks for closing
            running = False #ends loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update section
    all_sprites.update() #update all sprite


    #check to see if a bullet hits the mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #if mob or bullet hit gets deleted
    for hit in hits: #recreate mobs 
        score += 60 - hit.radius #score increase based on size
        random.choice(expl_sound).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    #check to see if a mob hits the player and hits is a list
                                                            #specifying what kind of collision 
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)#boolean controls whether 2nd parameter be deleted
    if hits: #checks if hits has smth
        running = False  
 

    # Draw/render section
    screen.fill(BLACK)
    screen.blit(background, background_rect) #blit is a term, copy pixel of the thing onto other thing
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    pygame.display.flip() #portion of the render is updated

pygame.quit()