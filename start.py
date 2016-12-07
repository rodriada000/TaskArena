import pygame
# Screen dimensions
SCR_WIDTH = 640
SCR_HEIGHT = 480

class MainView(object):
    
    def __init__(self, width=640, height=480, fps=30):
        """
        Initialize pygame, window, and font
        """
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height)) # Set screen size of pygame window
        self.allGroup = pygame.sprite.Group() # group of all sprites in view
        
    def run(self):
        """
        Main game loop
        """
        arena = Arena()
        player = Player((self.width/2,200), 90, 80, 90)
        player.level = arena
        self.allGroup.add(player, player.arm)
        running = True
        while running:
            seconds = self.clock.tick(self.fps) / 1000.0 # seconds passed since last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.goLeft(seconds)
                    if event.key == pygame.K_RIGHT:
                        player.goRight(seconds)
                    if event.key == pygame.K_UP:
                        player.jump()
 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()
            
            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                arena.shift_world(-diff)
     
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                arena.shift_world(diff)
            
            self.allGroup.clear(self.screen, arena.background)
            self.allGroup.update(seconds)
            arena.update()
            arena.draw(self.screen)
            self.allGroup.draw(self.screen)
            pygame.display.flip() # update pygame display
            
        pygame.quit() # clean up


class Player(pygame.sprite.Sprite):
    """
    """
    # image = pygame.image.load("Snake.gif")
    # image = image.convert_alpha()
    def __init__(self, startpos, hp, mana, stamina):
        super().__init__()
        
        # initialize stats
        self.health = hp
        self.mana = mana
        self.stamina = stamina
        self.strength = 1.0
        self.attackSpeed = 1.0
        self.netArmor = 0
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        
        self.pos = startpos
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        
        # create arm
        self.arm = Arm(self)
        
        self.level = None # list of sprites can bump into in current lvl
    
    def kill(self):
        """
        do other things before killing sprite
        """
        # stuff
        pygame.sprite.Sprite.kill(self)
        
    def update(self, seconds):
        """
        Update stats such as position of Player
        where seconds is time since last frame
        """
        # Gravity
        self.calcGravity(seconds)
 
        # Move left/right
        self.rect.x += self.change_x
 
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
        
        # update arm position
        self.arm.update(seconds)
 
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
 
    def calcGravity(self, seconds):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCR_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCR_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCR_HEIGHT:
            self.change_y = -8
 
    # Player-controlled movement:
    def goLeft(self, seconds):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
 
    def goRight(self, seconds):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        
class Arm(pygame.sprite.Sprite):
    """
    Represents the arm of a person.
    """
    def __init__(self, person):
        super().__init__()
        
        # Set speed vector of arm
        self.change_x = 0
        self.change_y = 0
        
        self.person = person
        self.pos = (self.person.rect.x/2, self.person.rect.y/2)
        
        # Create an image of the block, and fill it with a color.
        width = 15
        height = 55
        self.image = pygame.Surface([width, height])
        self.image.fill((173,43,255))
        self.rect = self.image.get_rect()
        

    def kill(self):
        """
        do other things before killing sprite
        """
        # stuff
        pygame.sprite.Sprite.kill(self)
        
    def update(self, seconds):
        """
        Update angle of arm based on mouse x,y coordinates
        where seconds is time since last frame
        """
        print(self.person.rect.x, ", ", self.person.rect.y)
        self.rect.x = self.person.rect.x
        self.rect.y = self.person.rect.y
    
class Weapon(pygame.sprite.Sprite):
    """
    Base class for weapons
    """

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()

class Arena():
    """
    This is a class used to define the Arena layout.
    """
 
    def __init__(self, player=None):
        self.platform_list = pygame.sprite.Group() # platforms in arena
        self.enemy_list = pygame.sprite.Group() # enemies in arena
        self.background = pygame.image.load("images/temp_bg.jpg").convert()
        # self.player = player
        
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            # block.player = self.player
            self.platform_list.add(block)
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    def update(self):
        """ Update everything in this arena."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this arena. """
        # Draw the background
        screen.fill((255,255,255))
        screen.blit(self.background,(self.world_shift // 3,0))
        
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

if __name__ == "__main__":
    game = MainView(SCR_WIDTH, SCR_HEIGHT, fps=60)
    game.run()
    