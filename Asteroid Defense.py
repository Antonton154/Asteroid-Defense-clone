import pygame
from random import random 

#initialize pygame  
pygame.init()

#screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

#caption    
pygame.display.set_caption("Asteroid Defense")

#icon
icon = pygame.image.load("images\icon.png")
pygame.display.set_icon(icon)

#background
background_image = pygame.image.load("images\\background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

#player
player_image = pygame.image.load("images\ship.png")
player_image = pygame.transform.scale(player_image, (screen_width/10, screen_width/10))
playerX = (screen_width-screen_width/10)/2
playerY = 480
player_change = 0.15
player_rect = player_image.get_rect()

def player(x,y):
    player_rect.x = x
    player_rect.y= y
    screen.blit(player_image, player_rect)

#asteroid
asteroid_image = pygame.image.load("images\\asteroid.png")

class asteroid:
    def __init__(self):
        self.asteroidX = random()*screen_width
        self.asteroidX_change = random()*0.15-0.075
        self.asteroidY_change = 0.5
        self.size = screen_width/10*(random()*1.5+0.5)
        self.asteroid_entity = pygame.transform.rotate(pygame.transform.scale(asteroid_image, (self.size, self.size)), random()*360)
        self.asteroid_entity.set_colorkey((255,255,255))
        self.asteroidY = 0
        self.rect = pygame.Rect(self.asteroidX, self.asteroidY, self.size, self.size)
    
    def move(self):
        self.asteroidX += self.asteroidX_change
        self.asteroidY += self.asteroidY_change
        self.rect.x = self.asteroidX
        self.rect.y = self.asteroidY

asteroids = []

def spawn_asteroid():
    asteroids.append(asteroid())

def update_asteroid(asteroid):
    screen.blit(asteroid.asteroid_entity, (asteroid.asteroidX, asteroid.asteroidY))

#spawn_asteroids
spawn_cooldown = 1000  # Cooldown period in milliseconds
last_spawn = 0    # Time that the ability was last used

#shield
shield = False
shield_start_time = 0
shield_duration = 3000

def shield_update():
    global current_time, shield, shield_duration, shield_start_time        
    if shield and current_time - shield_start_time >= shield_duration:
        shield = False

def hit():
    global current_time, shield, shield_duration, shield_start_time, lives
    if not shield:
        lives -= 1
        shield = True
        shield_start_time = current_time   

#check collision
colliding = False
def check_collision(player_rect, asteroids):
    global colliding, lives
    for asteroid in asteroids:
        if player_rect.colliderect(asteroid.rect):
            if not colliding:
                colliding = True
                hit()
                print(lives)
            return True
    colliding = False
    return False

#game set up
clock = pygame.time.Clock()
running = True
GameOver = False
lives = 3

while running and not GameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerX -= player_change
    if keys[pygame.K_d]:
        playerX += player_change
    if keys[pygame.K_w]:
        playerY -= player_change
    if keys[pygame.K_s]:
        playerY += player_change

    screen.blit(background_image, (0, 0)) 
    player(playerX,playerY)

    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720
    if playerY <=0:
        playerY = 0
    elif playerY >= 520:
        playerY = 520
    
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn > spawn_cooldown:
        last_spawn = current_time
        spawn_asteroid()

    for a in asteroids:
        a.move()
        update_asteroid(a)
        if a.asteroidX < 0 - a.size or a.asteroidX > screen_width or a.asteroidY>screen_height:
            asteroids.remove(a)
    shield_update()
    check_collision(player_rect, asteroids)

        

    pygame.display.update()
