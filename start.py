import pygame
from modules import player
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
        _player = player.Player((self.width/2,200), player.PlayerStats())
        _player.level = arena
        self.allGroup.add(_player.arm, _player)
        running = True
        while running:
            seconds = self.clock.tick(self.fps) / 1000.0 # seconds passed since last frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        _player.goLeft(seconds)
                    if event.key == pygame.K_RIGHT:
                        _player.goRight(seconds)
                    if event.key == pygame.K_UP:
                        _player.jump()
 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and _player.change_x < 0:
                        _player.stop()
                    if event.key == pygame.K_RIGHT and _player.change_x > 0:
                        _player.stop()
            
            # If the _player gets near the right side, shift the world left (-x)
            if _player.rect.right >= 500:
                diff = _player.rect.right - 500
                _player.rect.right = 500
                arena.shift_world(-diff)
     
            # If the _player gets near the left side, shift the world right (+x)
            if _player.rect.left <= 120:
                diff = 120 - _player.rect.left
                _player.rect.left = 120
                arena.shift_world(diff)
            
            self.allGroup.clear(self.screen, arena.background)
            self.allGroup.update(seconds)
            arena.update()
            arena.draw(self.screen)
            self.allGroup.draw(self.screen)
            pygame.display.flip() # update pygame display
            
        pygame.quit() # clean up
        
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
        level = [[500, 25, 0, 400],
                    [210, 70, 500, 500],
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
    