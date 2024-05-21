import pygame
import sys
pygame.init()

# Screen
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Naruto vs Sasuke")

# Colors
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
grey = (128,128,128)
yellow = (255,255,0)

# Images
walk_left_img = [
    pygame.image.load('pics/NL2.png'),
    pygame.image.load('pics/NL3.png'),
    pygame.image.load('pics/NL1.png')
]

walk_right_img = [
    pygame.image.load('pics/NR2.png'),
    pygame.image.load('pics/NR3.png'),
    pygame.image.load('pics/NR1.png')
]
enemy_left_img = [
    pygame.image.load('pics/SL2.png'),
    pygame.image.load('pics/SL3.png'),
    pygame.image.load('pics/SL1.png')
]

enemy_right_img = [
    pygame.image.load('pics/SR2.png'),
    pygame.image.load('pics/SR3.png'),
    pygame.image.load('pics/SR1.png')
]

bg_img = pygame.image.load('pics/bg.png')

naruto_logo = pygame.image.load('pics/Nh.png')
sasuke_logo = pygame.image.load('pics/Sh.png')
naruto_die_img = pygame.image.load('pics/Nd.png')
sasuke_die_img = pygame.image.load('pics/Sd.png')
ground_img = pygame.image.load('pics/ground.png')
ground_img = pygame.transform.scale(ground_img, (screen_width, 300))

# Fuction to display a text
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_loop():

    class Player():
        def __init__(self):
            self.x = 40
            self.y = 350
            self.width = 100
            self.height = 100
            self.speed = 8
            self.isjump = False
            self.jump_height = 10
            self.left = False
            self.right = False
            self.walk_count = 0
            self.standing = True
            self.hitbox = (self.x + 10, self.y + 6, 80, 80)
            self.health = 200
            self.die = False
            self.healthbar_color = green

        def draw(self):
            if self.walk_count+1 > 6:
                self.walk_count = 0

            if not self.die:
                if self.standing:
                    if self.left:
                        screen.blit(walk_left_img[2], (self.x, self.y))
                    elif self.right:
                        screen.blit(walk_right_img[2], (self.x, self.y))
                    else:
                        screen.blit(walk_right_img[2], (self.x, self.y))

                else:
                    if self.left:
                        screen.blit(walk_left_img[self.walk_count//2], (self.x, self.y))
                        self.walk_count += 1
                    if self.right:
                        screen.blit(walk_right_img[self.walk_count//2], (self.x, self.y))
                        self.walk_count += 1
            
            self.hitbox = (self.x + 10, self.y + 6, 80, 80)
            # pygame.draw.rect(screen, green, self.hitbox, 2)
            healthbar_back = pygame.draw.rect(screen, grey, (85, 40, 200, 20))
            healthbar_front = pygame.draw.rect(screen, self.healthbar_color, (85, 40, self.health, 20))
            screen.blit(naruto_logo, (10,8))

            if self.die:
                screen.blit(naruto_die_img, (self.x, self.y))
                screen.blit(enemy_left_img[2], (self.x, self.y))
                sasuke.moving = False
                draw_text("You Lose!", 50, red, 270, 220)
                draw_text("Press Enter to play again", 35, green, 220, 300)
                if keys[pygame.K_RETURN]:
                    game_loop()

        def hit(self):
            if not naruto.die:
                if self.health > 0:
                    self.health -= 10

                if self.health <=0:
                    self.die = True
                
                if self.health <= 100:
                    self.healthbar_color = yellow

                if self.health <= 30:
                    self.healthbar_color = red        

    class Weapon():
        def __init__(self, facing):
            self.x = naruto.x + naruto.width//2
            self.y = naruto.y + naruto.height//2 - 20
            self.width = 40
            self.height = 40
            self.vel = 7 * facing
            self.hitbox = (self.x, self.y, 40, 40)

        def draw(self):
            screen.blit(pygame.image.load('pics/shur.png'), (self.x, self.y))
            self.hitbox = (self.x, self.y, 40, 40)
            # pygame.draw.rect(screen, green, self.hitbox, 2)

    class Enemy():
        def __init__(self):
            self.x = screen_width - (100+40)
            self.y = 350
            self.width = 100
            self.height = 100
            self.speed = naruto.speed
            self.walk_count = 0
            self.left = True
            self.right = False
            self.hitbox = (self.x + 10, self.y + 6, 80, 80)
            self.health = 0
            self.moving = True
            self.healthbar_color = green
            self.die = False

        def draw(self):
            if self.walk_count+1 > 6:
                self.walk_count = 0

            if self.moving:
                if self.left:
                    screen.blit(enemy_left_img[self.walk_count//2], (self.x, self.y))
                    self.walk_count += 1 
                    self.x -= self.speed
                    if self.x < 0:
                        self.left = False
                        self.right = True

                if self.right:
                    screen.blit(enemy_right_img[self.walk_count//2], (self.x, self.y))
                    self.walk_count += 1
                    self.x += self.speed
                    if self.x > screen_width - self.width:
                        self.left = True
                        self.right = False

            if self.die:
                screen.blit(sasuke_die_img, (self.x, self.y))
                draw_text("You Win!", 50, green, 270, 220)
                draw_text("Press Enter to play again", 35, black, 220, 300)
                if keys[pygame.K_RETURN]:
                    game_loop()

            self.hitbox = (self.x + 10, self.y + 6, 80, 80)
            # pygame.draw.rect(screen, red, self.hitbox, 2)

            healthbar_front = pygame.draw.rect(screen, self.healthbar_color, (425, 40, 200, 20))
            healthbar_back = pygame.draw.rect(screen, grey, (425, 40, self.health, 20))
            screen.blit(sasuke_logo, (screen_width-(80+10),8))

        def hit(self):
            if self.health >= 0:
                self.health += 10

            if self.health >=200:
                self.moving = False
                self.die = True

            if self.health >= 100:
                self.healthbar_color = yellow 

                if self.health >= 170:
                    self.healthbar_color = red


    # Global Variables
    run = True
    clock = pygame.time.Clock()
    fps = 30
    shurikens = []
    naruto = Player()
    sasuke = Enemy()
    throw_speed = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if throw_speed > 0:
            throw_speed +=1
        if throw_speed > 3:
            throw_speed = 0

        # Moving Character
        keys = pygame.key.get_pressed()
        if not naruto.die and not sasuke.die:
            if keys[pygame.K_LEFT]:
                naruto.x -= naruto.speed
                naruto.standing = False
                naruto.left = True
                naruto.right = False
                
            elif keys[pygame.K_RIGHT]:
                naruto.x += naruto.speed
                naruto.standing = False
                naruto.right = True
                naruto.left = False

            else:
                naruto.standing = True
                naruto.walk_count = 0

            if not naruto.isjump:
                if keys[pygame.K_UP]:
                    naruto.isjump = True

            if naruto.isjump:
                if naruto.jump_height >= -10:
                    neg = 1

                    if naruto.jump_height < 0:
                        neg = -1

                    naruto.y -= (naruto.jump_height**2) * 0.5 * neg
                    naruto.jump_height -= 1

                else:
                    naruto.isjump = False
                    naruto.jump_height = 10

        # Making Boundries
        if naruto.x < 0:
            naruto.x = 0
        if naruto.x > screen_width - naruto.width:
            naruto.x = screen_width - naruto.width

        # Throwing Shurikens
        for shuriken in shurikens:
            if shuriken.x > 0 and shuriken.x < screen_width:
                shuriken.x += shuriken.vel
            else:
                shurikens.pop(shurikens.index(shuriken))

            # Collison of Shurikens with Sasuke
            if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > sasuke.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < sasuke.hitbox[1] + sasuke.hitbox[3]:
                if shuriken.hitbox[0] + shuriken.hitbox[2]/2 > sasuke.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                    shurikens.pop(shurikens.index(shuriken))
                    sasuke.hit()

        # Collison of Naruto with Sasuke
        if naruto.hitbox[1] + naruto.hitbox[3]//2 > sasuke.hitbox[1] and naruto.hitbox[1] + naruto.hitbox[3]//2 < sasuke.hitbox[1] + sasuke.hitbox[3]:
            if naruto.hitbox[0] + naruto.hitbox[2]//2 > sasuke.hitbox[0] and naruto.hitbox[0] + naruto.hitbox[2] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                naruto.hit()

        screen.blit(bg_img, (0,0))
        # screen.blit(ground_img, (0, 200))
        naruto.draw()
        sasuke.draw()

        # Throwning Shurikens
        if keys[pygame.K_SPACE] and throw_speed == 0:
            if naruto.left == True:
                facing = -1
            else:
                facing = 1

            if len(shurikens) < 3:
                shurikens.append(Weapon(facing))
            throw_speed = 1
                
        for shuriken in shurikens:
            shuriken.draw()
        # pygame.draw.rect(screen, white, [player_x, player_y, player_width, player_height])
        clock.tick(fps)
        pygame.display.update()

game_loop()
pygame.quit()