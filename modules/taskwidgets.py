"""
Module to define all classes/widgets related to Tasks
"""
import pygame
from pygame.locals import *
from pgu import gui

class Task():
    """
    Class that represents a task user can create.
    Task has name, notes, dueDate, tags properties
    """
    def __init__(self, name=None, notes=None, duedate=None, tags=None):
        """
        Create new Task
        """
        self.name = name
        self.notes = notes
        self.dueDate = duedate
        self.tags = tags
    

class TaskList(gui.Table):
    """
    represents a scrollable list of Tasks.
    this widget is responsible for displaying user's tasks
    along with creating buttons to interact with the tasks
    """
    def __init__(self, doneFnc=None, editFnc=None, removeFnc=None,**params):
        """
        Initialize TaskList with three callbacks:
            doneFnc -- callback when 'Done' button is clicked
            editFnc -- callback when 'Edit' button is clicked
            removeFnc -- callback when 'Remove' button is clicked
        These three callbacks should be defined functions
        in the parent widget with parameters (task, task_index)
        """
        gui.Table.__init__(self,**params)
        self.tasks = [] # list of Tasks
        self.editFnc = editFnc
        self.removeFnc = removeFnc
        self.doneFnc = doneFnc
        
    def addTask(self, task):
        """
        Add a task to the list and add to UI
        """
        self.tasks.append(task)
        self.createTaskItem(len(self.tasks)-1)
        
    def updateTask(self, updated_task, task_index):
        """
        Update Task in task list at given task_index with updated_task.
        """
        self.tasks[task_index] = updated_task
        self.updateList()
    
    def removeTask(self, task_index):
        """
        Remove Task in task list at given task_index
        """
        del self.tasks[task_index]
        self.updateList()
        self.repaint()

    def createTaskItem(self, task_index):
        """
        Creates a row in the Table to represent a Task.
        Displays Task name, along with 'Done','Edit','Remove' button
        """
        self.tr()
        self.td(gui.Label(self.tasks[task_index].name), colspan=3, align=-1)
        self.td(gui.Spacer(width=50,height=1))
        
        doneBtn = gui.Button("Done")
        doneBtn.connect(pygame.MOUSEBUTTONUP, self.doneFnc, self.tasks[task_index], task_index)
        self.td(doneBtn, align=0)
        
        editBtn = gui.Button("Edit")
        editBtn.connect(gui.CLICK, self.editFnc, self.tasks[task_index], task_index)
        self.td(editBtn, align=0)
        
        removeBtn = gui.Button("Remove")
        removeBtn.connect(gui.CLICK, self.removeFnc, self.tasks[task_index], task_index)
        self.td(removeBtn, align=0)

    
    def updateList(self):
        """
        Will update the UI to display updated task list.
        """
        self.clear() # clear old list
        print('num tasks:', len(self.tasks))
        if len(self.tasks) == 0:
            self.tr()
        else:
            for i in range(0, len(self.tasks)): # redraw updated list
                self.createTaskItem(i)
        
        
class TaskDialog(gui.Dialog):
    """
    Dialog to create a new task or edit existing task
    """
    def __init__(self,**params):
        self.task = gui.Form() # widget values get added to this dict
        self.state = None
        title = gui.Label("Task Dialog")
        table = gui.Table(width=400)
        
        # Name input
        table.tr()
        table.td(gui.Label("Name:"), colspan=1)
        table.td(gui.Input(name="name"), colspan=3)
        table.tr()
        table.td(gui.Spacer(width=1,height=5))
        
        # Notes input
        table.tr()
        table.td(gui.Label("Notes:"), colspan=1)
        table.td(gui.Input(name="notes"), colspan=3)
        table.tr()
        table.td(gui.Spacer(width=1,height=5))
        
        # Due date input
        table.tr()
        table.td(gui.Label("Due Date:"), colspan=1)
        table.td(gui.Input(name="dueDate"), colspan=3)
        table.tr()
        table.td(gui.Spacer(width=1,height=5))
        
        # tags checkbox
        table.tr()
        table.td(gui.Label("Tags:"), colspan=4, align=0)
        
        tagGroup = gui.Group(name="tags")
        table.tr()
        table.td(gui.Label("School"), colspan=2, align=1)
        table.td(gui.Checkbox(tagGroup,value="school"))
        
        table.tr()
        table.td(gui.Label("Work"), colspan=2, align=1)
        table.td(gui.Checkbox(tagGroup,value="work"))
        
        table.tr()
        table.td(gui.Label("Health"), colspan=2, align=1)
        table.td(gui.Checkbox(tagGroup,value="health"))
        
        
        table.tr()
        table.td(gui.Spacer(width=1,height=10))
        table.tr()
        self.saveBtn = gui.Button("Add Task")
        self.saveBtn.connect(gui.CLICK,self.send,gui.CHANGE)
        table.td(self.saveBtn, colspan=4)

        gui.Dialog.__init__(self,title,table)

    def clearForm(self):
        """
        Clear the forms values
        """
        for k,v in self.task.items():
            if isinstance(self.task[k].value, list):
                self.task[k].value = []
            else:
                self.task[k].value = ""
                
    def fillForm(self, task):
        """
        Fill form out with task values
        """
        for k,v in self.task.items():
            self.task[k].value = task.__dict__[k]
            
    def getTask(self):
        """
        return a Task object created with
        values in dialog
        """
        t = Task()
        for k,v in self.task.items():
            t.__dict__[k] = v
        return t
        
    def updateState(self, new_state):
        """
        Update the state of the dialog, either 'new' or 'edit' state.
        Updates the ui button based on new state
        """
        self.state = new_state
        if self.state == "edit":
            self.saveBtn.value = "Save"
        elif self.state == "new":
            self.saveBtn.value = "Add"
            self.clearForm() # clear form for new task