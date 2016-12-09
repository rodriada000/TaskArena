import pygame
from pygame.locals import *
from pgu import gui
from tinydb import TinyDB
from modules import taskwidgets, player, statwidget

# Screen dimensions
SCR_WIDTH = 640
SCR_HEIGHT = 480

        

class MainMenu(gui.Desktop):
    def debugKeys(self):
        keys=pygame.key.get_pressed()
        if keys[K_u]: # TEST LEVELING UP
            self._player.addExperience(10)
            self.statsTable.updateStats(self._player)
            
    def __init__(self,**params):
        gui.Desktop.__init__(self,**params)
        self.connect(gui.QUIT,self.saveAndQuit)
        self.connect(pygame.KEYDOWN, self.debugKeys) #DEBUG purposes
        layout = gui.Table(width=SCR_WIDTH,height=SCR_HEIGHT)
        
        # Create a TaskList
        self.taskList = taskwidgets.TaskList(editFnc=self.editTask, doneFnc=self.completeTask, removeFnc=self.removeTask,
                                    width=400, height=420, style={'border':1})
        # load user data
        self.loadTasks()
        self._player = self.loadPlayerStats()
        
        # initialize dialogs
        self.taskDialog = taskwidgets.TaskDialog()
        self.taskDialog.connect(gui.CHANGE,self.diagOnChange)
        
        # add TaskList to MainMenu
        self.selectedTask = None
        layout.tr()
        layout.td(gui.Spacer(width=5,height=5))
        layout.td(self.taskList, align=-1, colspan=5, rowspan=6)
        
        # Add StatTable to MainMenu
        self.statsTable = statwidget.StatTable(self._player, width=200)
        layout.td(self.statsTable, col=6, colspan = 3,row=3, rowspan=2, style={'border':1})
        layout.td(gui.Spacer(width=10,height=5), row=3, col=9)
        
        # Add 'Upgrade Skills' and 'Inventory' button
        upgradeBtn = gui.Button("Upgrade Skills")
        upgradeBtn.connect(gui.CLICK, self.openStatsDialog)
        inventoryBtn = gui.Button("Inventory")
        
        layout.td(upgradeBtn, row=5, col=6, valign=-1)
        layout.td(gui.Spacer(width=5,height=5), row=5, col=7)
        layout.td(inventoryBtn, row=5, col=8, valign=-1)
        
        newTaskBtn = gui.Button("New Task")
        newTaskBtn.connect(gui.CLICK, self.newTask)
        
        fightBtn = gui.Button("Fight")
        quitBtn = gui.Button("Quit")
        quitBtn.connect(gui.CLICK, self.saveAndQuit)
        
        layout.tr()
        layout.td(gui.Spacer(width=400,height=1), row=6,colspan=6)
        layout.td(newTaskBtn, row=6)
        layout.td(fightBtn, row=6)
        layout.td(quitBtn, row=6)
        
        self.widget = layout
        
        
    def saveAndQuit(self):
        """
        Save tasks and player stats to DB files
        and quit game
        """
        self.saveTasks()
        self.savePlayerStats()
        self.quit()
        
        
    def savePlayerStats(self):
        """
        Save player stats to playerDB file
        """
        playerDB = TinyDB('data/playerDB.json')
        playerDB.purge() # remove old stats
        record = {'hp': self._player.hp, 'mana': self._player.mana,
                'stamina': self._player.stamina, 'strength': self._player.strength,
                'atkSpeed': self._player.atkSpeed, 'netArmor': self._player.netArmor,
                'xp': self._player.xp, 'skillPts': self._player.skillPts, 'lvl': self._player.lvl,
                'xpNeeded': self._player.xpNeeded}
        playerDB.insert(record)
        
    def saveTasks(self):
        """
        Saves all tasks in TaskList to the taskDB file
        """
        taskDB = TinyDB('data/taskData.json')
        taskDB.purge()
        for task in self.taskList.tasks:
            record = {'name': task.name, 'notes': task.notes,
                    'dueDate': task.dueDate, 'tags': task.tags } # tinydb expects data to be dicts
            taskDB.insert(record)
        
    def loadTasks(self):
        """
        Loads users tasks from db into program
        """
        taskDB = TinyDB('data/taskData.json')
        allTasks = taskDB.all()
        for record in allTasks: # reconstruct Task object from dict
            t = taskwidgets.Task(name=record['name'], notes=record['notes'],
                        duedate=record['dueDate'], tags=record['tags'])
            self.taskList.addTask(t)
            
    def loadPlayerStats(self):
        """
        Load the user's player stats into memory from db
        returns a PlayerStats object
        """
        playerDB = TinyDB('data/playerDB.json')
        records = playerDB.all()
        if len(records) == 0:
            return player.PlayerStats() # no stats for player, load default
        else:
            stats = player.PlayerStats(hp=records[0]['hp'], mana=records[0]['mana'],
                    stamina=records[0]['stamina'], strength=records[0]['strength'],
                    atkSpeed=records[0]['atkSpeed'], armor=records[0]['netArmor'],
                    xp=records[0]['xp'], skillPts=records[0]['skillPts'], lvl=records[0]['lvl'],
                    xpNeeded=records[0]['xpNeeded'])
            return stats
        
    def editTask(self, task, task_index):
        self.selectedTask = task_index
        self.taskDialog.updateState("edit")
        self.taskDialog.fillForm(task)
        self.taskDialog.open()
        
    # TODO: fix bug where removing last task in list causes asserstion error
    def completeTask(self, task, task_index):
        """
        callback for completing tasks in TaskList
        """
        self.selectedTask = task_index
        # do stuff to give xp to character and update DB
        self.taskList.removeTask(task_index)
        
    def removeTask(self, task, task_index):
        """
        callback for removing tasks from TaskList
        """
        self.selectedTask = task_index
        # do stuff to update DB
        self.taskList.removeTask(task_index)
        
    def newTask(self):
        self.taskDialog.updateState("new")
        self.taskDialog.open()
        
    def diagOnChange(self):
        """
        callback when TaskDialog is closed by user clicking 'add' button'
        If TaskDialog state is 'new' then the task from TaskDialog will be added
        to the TaskList. When the state is 'edit', a task in TaskList will be updated.
        """
        t = self.taskDialog.getTask()
        if self.taskDialog.state == "new":
            self.taskList.addTask(t)
        elif self.taskDialog.state == "edit":
            self.taskList.updateTask(t, self.selectedTask)
        self.taskDialog.close()
        
    def openStatsDialog(self):
        """
        Open the 'Upgrade Stats' dialog for user to upgrade
        character skills with skill points.
        """
        statsDiag = statwidget.UpgradeStatsDialog(self._player) # create dialog
        statsDiag.connect(gui.CHANGE, self.saveStats, statsDiag) # connect dialog to save function
        statsDiag.open()
        
    def saveStats(self, dialog):
        """
        Save the players new stats from the UpgradeStatsDialog
        and upate the UI
        """
        self._player = dialog.stats
        dialog.close()
        self.statsTable.updateStats(self._player)

if __name__ == '__main__':
    app = MainMenu()
    app.run()