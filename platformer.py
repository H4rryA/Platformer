import pygame

WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent's constructor
        super(Player, self).__init__()
        self.images = []
        for i in range(7):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\viking"+str(i)+".png")
            img = pygame.transform.scale(img, (40, 52))
            self.images.append(img)
        for i in range(7, 10):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\viking"+str(i)+".png")
            img = pygame.transform.scale(img, (54, 48))
            self.images.append(img)
        for i in range(10, 12):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\viking"+str(i)+".png")
            img = pygame.transform.scale(img, (62, 48))
            self.images.append(img)

        self.image = self.images[0]
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        self.hp = 10

        self.hit = False

        self.count = 0
        # List of sprites we can bump against
        self.level = None

        #Initializes Score
        self.score = 0

        self.damage = 5

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        #Coin hit registry
        coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, True)
        for coin in coin_hit_list:
            self.score += 1

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def attack(self, dir):
        if(dir == 1):
            self.rect.x -= 30
            enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            self.rect.x += 30
        if(dir == 2):
            self.rect.x += 30
            enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            self.rect.x -= 30
        for enemy in enemy_hit_list:
            self.hit = True

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent's constructor
        super(Enemy, self).__init__()

        self.images = []
        for i in range(4):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\samurai"+str(i)+".png")
            img = pygame.transform.scale(img, (58,48))
            self.images.append(img)
        for i in range(4, 7):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\samurai"+str(i)+".png")
            img = pygame.transform.scale(img, (72,46))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.count = 0

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        self.hp = 5

        self.shift = 0

    def update(self):
        self.rect.x += self.change_x
        if(self.hp <= 0):
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin, self).__init__()
        self.images = []
        for i in range(1,10):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\coin"+str(i)+".png")
            img = pygame.transform.scale(img, (32, 32))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.count = 0

class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super(Flag, self).__init__()
        self.images = []
        for i in range(9):
            img = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\\flag"+str(i)+".png")
            img = pygame.transform.scale(img, (40, 52))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.count = 0

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super(Platform, self).__init__()

        #self.image = pygame.Surface([width, height])
        image = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\wall.png")
        rect = (0, 0, width, height)
        self.image = pygame.transform.chop(image, rect)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
        collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.player = player

        self.flag = None

        self.enemy = None
        # Background image
        self.background = pygame.image.load("C:\\Users\\Harry\\Documents\\GitHub\\Platformer\\img\space.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.world_shift = 0

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.coin_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for coin in self.coin_list:
            coin.rect.x += shift_x

# Create platforms for the level
class Level_01(Level):
    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -2390

        # Array with width, height, x, and y of platform
        level = [[210, 70, 200, 300],
                [210, 70, 500, 500],
                [210, 70, 800, 400],
                [210, 70, 1000, 500],
                [210, 70, 1120, 280],
                [210, 70, 1400, 400],
                [210, 70, 1700, 300],
                [210, 70, 2000, 500],
                [210, 70, 2175, 350],
                [210, 70, 2300, 200],
                [210, 70, 2600, 400],
                [210, 70, 3000, 300],
                [210, 70, 3300, 175]
                 ]

        enemies = [[550, 453],
                    [1140, 233],
                    [2040, 453],
                    [2640, 353],
                    [3030, 253]
                    ]

        reward = [[500, 475],
                [800, 350],
                [1000, 460],
                [1120, 250],
                [1700, 200],
                [1900, 400],
                [2100, 300],
                [2800, 200],
                [3000, 100]
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        for coin in reward:
            circle = Coin()
            circle.rect.x = coin[0]
            circle.rect.y = coin[1]
            self.coin_list.add(circle)

        for enemy in enemies:
            en = Enemy()
            en.rect.x = enemy[0]
            en.rect.y = enemy[1]
            self.enemy_list.add(en)

        self.flag = Flag()
        self.flag.rect.x = 3510
        self.flag.rect.y = 125
        self.coin_list.add(self.flag)

def main():
    """ Main Program """
    pygame.init()
    font = pygame.font.SysFont("arial", 15, "bold")

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    #Player spawn location
    player.rect.x = 200
    player.rect.y = 200
    active_sprite_list.add(player)

    done = False
    # Loop until the user clicks the close button.
    cycletime = 0
    stop = True
    attackRight = False
    attackLeft = False
    flip = False
    move = 2
    ch = 60
    win = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_RIGHT:
                    player.attack(2)
                    attackRight = True
                if event.key == pygame.K_LEFT:
                    player.attack(1)
                    attackLeft = True
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                    stop = True
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                    stop = True

        score = font.render("Score: " + str(player.score) , 1, WHITE)
        hp = font.render("HP: " + str(player.hp), 1, WHITE)

        # Update the player.
        #Changes the image
        clock.tick(60)
        ms = clock.get_time()
        cycletime += ms/5
        if cycletime > 15:

            if(player.hit == True):
                enemy.hp -= player.damage
                player.score += player.damage
                player.hit = False

            if player.rect.y >= SCREEN_HEIGHT - player.rect.height:
                done = True
            if player.change_y <0:
                player.count = 6
            elif player.change_y>0:
                if(player.count < 9):
                    player.count += 1
                else:
                    player.count = 7
            elif player.change_x != 0:
                if(player.count <= 4):
                    player.count += 1
                else:
                    player.count = 0
            elif(attackRight == True):
                if(player.count == 10):
                    player.count = 11
                    attackRight = False
                else:
                    player.count = 10
            elif(attackLeft == True):
                flip = True
                if(player.count == 10):
                    player.count = 11
                    attackLeft = False
                else:
                    player.count = 10
            elif stop == True:
                player.count = 0
            player.image = player.images[player.count]

            for coin in current_level.coin_list:
                coin.count+=1
                if(coin.count == 9):
                    coin.count = 1
                coin.image = coin.images[coin.count]

            for enemy in current_level.enemy_list:
                enemy.rect.x += ch
                block_hit_list = pygame.sprite.spritecollide(enemy, current_level.platform_list, False)
                enemy.rect.x -= ch
                contains = False
                for block in block_hit_list:
                    enemy.rect.x+= move
                    contains = True
                if(contains == False):
                    enemy.rect.x+= -move
                    move = move * -1
                    ch = ch * -1

                enemy.count+=1
                if(enemy.count == 7):
                    enemy.count = 0
                enemy.image = enemy.images[enemy.count]
                if(move < 0):
                    enemy.image = pygame.transform.flip(enemy.images[enemy.count], True, False)
                    if(enemy.count ==4):
                        enemy.rect.x -= 14
                    elif(enemy.count == 0):
                        enemy.rect.x += 14
                if(enemy.count >= 4):
                    enemy_attack_list = pygame.sprite.spritecollide(player, current_level.enemy_list, False)
                    if len(enemy_attack_list) > 0 and player.hit == False:
                        player.hp -= 2
                        player.rect.x -= 50
                    if player.hp <= 0:
                        done = True


            if(player.change_x < 0 or flip==True):
                player.image = pygame.transform.flip(player.image, True, False)
                flip = False
            cycletime = 0

        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 600:
            diff = player.rect.right -600
            player.rect.right = 600
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 100:
            diff = 100 - player.rect.left
            player.rect.left = 100
            current_level.shift_world(diff)

        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            done = True
            win = True

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.blit(current_level.background,(0, 0))
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        screen.blit(score, (10, 10))
        screen.blit(hp, (90, 10))
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


    screen.fill((0, 0, 0))
    if(win == True):
        gameover = font.render("You Win! Score: " + str(player.score), 1, WHITE)
    else:
        gameover = font.render("Game Over! Score: " + str(player.score), 1, WHITE)
    screen.blit(gameover, (350, 300))
    pygame.display.flip()
    pygame.time.wait(2000)
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
