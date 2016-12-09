"""
Module to define the stats window widget
"""
import pygame
from pygame.locals import *
from pgu import gui
from copy import copy

class StatTable(gui.Table):
    """
    Inherits from Table. creates a table to display
    stats of the player
    """
    def __init__(self, stats, **params):
        """
        Initialize StatTable with the given stats
        """
        gui.Table.__init__(self,**params)
        
        # Health row
        self.tr()
        self.td(gui.Label("Max HP:"), align=-1)
        self.hpLabel = gui.Label(str(stats.hp))
        self.td(self.hpLabel)

        # Mana row
        self.tr()
        self.td(gui.Label("Max Mana:"), align=-1)
        self.manaLabel = gui.Label(str(stats.mana))
        self.td(self.manaLabel)
        
        # Stamina row
        self.tr()
        self.td(gui.Label("Max Stamina:"), align=-1)
        self.staminaLabel = gui.Label(str(stats.stamina))
        self.td(self.staminaLabel)
        
        # Strength row
        self.tr()
        self.td(gui.Label("Strength:"), align=-1)
        self.strLabel = gui.Label("{:.2f}".format(stats.strength))
        self.td(self.strLabel)
        
        # Attack Speed row
        self.tr()
        self.td(gui.Label("Attack Speed:"), align=-1)
        self.speedLabel = gui.Label("{:.2f}".format(stats.atkSpeed))
        self.td(self.speedLabel)
        
        # Armor row
        self.tr()
        self.td(gui.Label("Armor:"), align=-1)
        self.armorLabel = gui.Label(str(stats.netArmor))
        self.td(self.armorLabel)
        
        # XP row
        self.tr()
        self.td(gui.Label("Experience:"), align=-1)
        self.xpLabel = gui.Label(str(stats.xp) + " / " + str(stats.xpNeeded))
        self.td(self.xpLabel)
        
        # Level row
        self.tr()
        self.td(gui.Label("Level:"), align=-1)
        self.lvlLabel = gui.Label(str(stats.lvl))
        self.td(self.lvlLabel)
        
        # Available skill points row
        self.tr()
        self.td(gui.Label("Available Skill Points:"), align=-1)
        self.skillLabel = gui.Label(str(stats.skillPts))
        self.td(self.skillLabel)
        
    def updateStats(self, stats):
        """
        update the values of stats with the new given stats
        """
        self.hpLabel.set_text(str(stats.hp))
        self.manaLabel.set_text(str(stats.mana))
        self.staminaLabel.set_text(str(stats.stamina))
        self.strLabel.set_text("{:.2f}".format(stats.strength))
        self.speedLabel.set_text("{:.2f}".format(stats.atkSpeed))
        self.armorLabel.set_text(str(stats.netArmor))
        self.xpLabel.set_text(str(stats.xp) + " / " + str(stats.xpNeeded))
        self.lvlLabel.set_text(str(stats.lvl))
        self.skillLabel.set_text(str(stats.skillPts))
        

class UpgradeStatsTable(gui.Table):
    """
    Inherits from Table. Displays stats and allow user
    to upgrade them using skill points
    """
    def __init__(self, stats, **params):
        """
        Initialize StatTable with the given stats
        and set up buttons
        """
        gui.Table.__init__(self, **params)
        self.baseStats = stats # keep reference to original player stats
        self.updatedStats = copy(stats) # the new stats of player
        self.increments = {'hp':5, 'mana':5, 'stamina':5,'strength':0.1, 'atkSpeed':0.05} # how much to add/subtract for each skill
        self.usedPts = {'hp':0, 'mana':0, 'stamina':0,'strength':0, 'atkSpeed':0} # points that have been used corresponding to stat that used it
        
        spacer = gui.Spacer(width=5, height=5)
        # Health row
        plusBtn = gui.Button("+")
        plusBtn.connect(gui.CLICK, self.plusBtnClicked, 'hp')
        minusBtn = gui.Button("-")
        minusBtn.connect(gui.CLICK, self.minusBtnClicked, 'hp')
        self.tr()
        self.td(gui.Label("Max HP:"), align=-1)
        self.hpLabel = gui.Label(str(stats.hp))
        self.td(minusBtn)
        self.td(spacer)
        self.td(self.hpLabel)
        self.td(spacer)
        self.td(plusBtn)

        # Mana row
        plusBtn = gui.Button("+")
        plusBtn.connect(gui.CLICK, self.plusBtnClicked, 'mana')
        minusBtn = gui.Button("-")
        minusBtn.connect(gui.CLICK, self.minusBtnClicked, 'mana')
        self.tr()
        self.td(gui.Label("Max Mana:"), align=-1)
        self.manaLabel = gui.Label(str(stats.mana))
        self.td(minusBtn)
        self.td(spacer)
        self.td(self.manaLabel)
        self.td(spacer)
        self.td(plusBtn)

        # Stamina row
        plusBtn = gui.Button("+")
        plusBtn.connect(gui.CLICK, self.plusBtnClicked, 'stamina')
        minusBtn = gui.Button("-")
        minusBtn.connect(gui.CLICK, self.minusBtnClicked, 'stamina')
        self.tr()
        self.td(gui.Label("Max Stamina:"), align=-1)
        self.staminaLabel = gui.Label(str(stats.stamina))
        self.td(minusBtn)
        self.td(spacer)
        self.td(self.staminaLabel)
        self.td(spacer)
        self.td(plusBtn)
        
        # Strength row
        plusBtn = gui.Button("+")
        plusBtn.connect(gui.CLICK, self.plusBtnClicked, 'strength')
        minusBtn = gui.Button("-")
        minusBtn.connect(gui.CLICK, self.minusBtnClicked, 'strength')
        self.tr()
        self.td(gui.Label("Strength:"), align=-1)
        self.strLabel = gui.Label("{:.2f}".format(stats.strength))
        self.td(minusBtn)
        self.td(spacer)
        self.td(self.strLabel)
        self.td(spacer)
        self.td(plusBtn)
        
        # Attack Speed row
        plusBtn = gui.Button("+")
        plusBtn.connect(gui.CLICK, self.plusBtnClicked, 'atkSpeed')
        minusBtn = gui.Button("-")
        minusBtn.connect(gui.CLICK, self.minusBtnClicked, 'atkSpeed')
        self.tr()
        self.td(gui.Label("Attack Speed:"), align=-1)
        self.speedLabel = gui.Label("{:.2f}".format(stats.atkSpeed))
        self.td(minusBtn)
        self.td(spacer)
        self.td(self.speedLabel)
        self.td(spacer)
        self.td(plusBtn)
        
        # Available skill points row
        self.tr()
        self.td(gui.Label("Available Skill Points:"), align=-1)
        self.skillLabel = gui.Label(str(stats.skillPts))
        self.td(self.skillLabel)
        
    def plusBtnClicked(self, stat):
        """
        callback for when '+' button is clicked. increment
        the selected stat's value.
        """
        if self.updatedStats.skillPts == 0:
            return # no skill points available
        
        values = {'hp':5, 'mana':5, 'stamina':5,'strength':0.1, 'atkSpeed':0.05}
        self.updatedStats.__dict__[stat] += values[stat] # increment the selected stat
        self.usedPts[stat] += 1 # skill point used
        self.updatedStats.skillPts -= 1 # remove one from availabe
        self.updateStatsUI()
        
    def minusBtnClicked(self, stat):
        """
        callback for when '-' button is clicked. subtract
        from selected stat's value.
        """
        if self.usedPts[stat] == 0:
            return # no skill points used for that stat
        
        self.updatedStats.__dict__[stat] -= self.increments[stat] # increment the selected stat
        self.updatedStats.skillPts += 1 # skill point now avaible
        self.usedPts[stat] -= 1 # one less used up pt for stat
        
        self.updateStatsUI()
        
    def updateStatsUI(self):
        """
        update the UI to show updated stats
        """
        self.hpLabel.set_text(str(self.updatedStats.hp))
        self.manaLabel.set_text(str(self.updatedStats.mana))
        self.staminaLabel.set_text(str(self.updatedStats.stamina))
        self.strLabel.set_text("{:.2f}".format(self.updatedStats.strength))
        self.speedLabel.set_text("{:.2f}".format(self.updatedStats.atkSpeed))
        self.skillLabel.set_text(str(self.updatedStats.skillPts))
        
class UpgradeStatsDialog(gui.Dialog):
    """
    Dialog to let the user upgrade their character stats.
    Makes use of UpgradeStatsTable.
    """
    def __init__(self, player_stats, **params):
        title = gui.Label("Upgrade Stats Dialog")
        table = UpgradeStatsTable(player_stats)
        self.stats = table.updatedStats
        self.saveBtn = gui.Button("Save")
        self.saveBtn.connect(gui.CLICK,self.send,gui.CHANGE)
        
        table.tr()
        table.td(self.saveBtn, colspan=table.getColumns(), align=0)

        gui.Dialog.__init__(self,title,table)
