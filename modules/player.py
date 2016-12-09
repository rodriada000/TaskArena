import pygame
from math import atan2, degrees, floor
"""
Module to define the Player class, and PlayerStats class
"""
SCR_WIDTH = 640
SCR_HEIGHT = 480

class PlayerStats():
    """
    class to contain player stats and compute experience
    """
    def __init__(self, hp=100, mana=100, stamina=100, strength=1.0,
                atkSpeed=1.0, armor=0, xp=0, skillPts=0, lvl=0, xpNeeded=50):
        self.hp = hp
        self.mana = mana
        self.stamina = stamina
        self.strength = strength
        self.atkSpeed = atkSpeed
        self.netArmor = armor
        self.xp = xp # players amount of experience
        self.xpNeeded = xpNeeded # amount of experience needed to level up
        self.skillPts = skillPts # number of skill points player has available to spen
        self.lvl = lvl # players current level
        
    def addExperience(self, xp):
        """
        Increments the players experience by xp amount.
        Will level up player if they have enough experience.
        """
        self.xp += xp
        if self.xp >= self.xpNeeded:
            self.LevelUpPlayer()
    
    def LevelUpPlayer(self):
        """
        Level up the player by 1 and give them 1 skill point.
        Also compute how much xp is needed to reach next level.
        """
        self.lvl += 1
        self.skillPts += 1
        percent = 0.5
        if self.lvl > 8:
            percent = 0.45 # reduce how much xp is added once higher level
        elif self.lvl > 16:
            percent = 0.4
        elif self.lvl > 25:
            percent = 0.3
        self.xpNeeded = floor(self.xpNeeded + self.xpNeeded * percent)

class Player(pygame.sprite.Sprite):
    """
    """
    # image = pygame.image.load("Snake.gif")
    # image = image.convert_alpha()
    def __init__(self, startpos, stats):
        super().__init__()
        
        # initialize stats
        self.stats = stats
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        
        self.pos = startpos
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
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
    Represents the arm of the player.
    """
    def __init__(self, player):
        super().__init__()
        
        # Set speed vector of arm
        self.change_x = 0
        self.change_y = 0
        
        self.player = player
        # self.pos = (self.player.rect.x/2, self.player.rect.y/2)
        
        # Create an image of the block, and fill it with a color.
        self.width = 60
        self.height = 10
        self.orig_image = pygame.image.load("images/temp_arm.png").convert_alpha()
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 8)
        self.rect.x = self.player.rect.x + self.player.width/2
        self.rect.y = self.player.rect.y + self.player.height/2
        self.angle = 0

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
        oldCenter = self.rect.center
        print("center:", (self.player.rect.centerx, self.player.rect.centery))
        self.update_angle(pygame.mouse.get_pos())
        
        # update rectangle angle
        oldrect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.orig_image, self.angle*-1)
        self.rect = self.image.get_rect(center=(0,8))

        self.rect.x = self.player.rect.x + self.player.width/2
        self.rect.y = self.player.rect.y + self.player.height/3
        
    def update_angle(self, mouse):
        """
        Find the new angle between the center of player and the mouse.
        """
        offset = (mouse[1]-self.player.rect.centery, mouse[0]-self.player.rect.centerx)
        self.angle = degrees(atan2(*offset))
        print("angle:", self.angle)