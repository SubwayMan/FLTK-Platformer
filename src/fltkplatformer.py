#imports    
from fltk import *
from globs import *
from GameWidget import *

#--------------------------HEADER--------------------------
#This is the main script launcher of the program, controlling
#the timeline and structure of the game. 
#The FRAMEWORK class handles scene management, switching from
#main menu screen to the actual level.
#The level class is responsible for structuring its contents
#and calculating/evaluating the game loop.
class Level(Fl_Group):

    """Level class. Constructor self(r, c, s, bg, endfunc):
r: rows, c: columns, s: level string, bg: background.
endfunc: listener function to which level object can notify of
level ending.
Inherits from an FLTK group.
LIMITATIONS:
r*c = len(s)"""
    def __init__(self, r, c, s, bg, endfunc) -> None:
        """Constructor.""" 
        #inherit from FLTK's group class
        Fl_Group.__init__(self, 0, 0, 32*(c-2), 32*(r-2))
        #prep array for objects
        self.objects = []
        #create variable to store player instance 
        self.chara = None
        #character map to the resulting game object.
        self.idtomod = {
            "X": Solid_Block,
            "^": Sawblade,
            "*": exitportal,
            "=": jumppad,
            "k": chest_key
            }
        #Store listener function 
        self.endfunc = endfunc
        #Begin drawing  
        self.begin()
        #Create background canvas
        self.bg = Fl_Box(0, 0, 32*(c-2), 32*(r-2))
        #Set background        
        self.bg.image(Fl_JPEG_Image(os.path.join(ASSETS, bg)).copy(self.bg.w(), self.bg.h()))
        #For calculating number of required keys for player 
        keys = 0
        #Go through provided textmap
        for row in range(r):
            for col in range(c):
                #Get character   
                id = s[(row*c)+col]
                #Special case for player class                
                if id == "@":
                    self.chara = player((col*32)-32, (row*32)-32, 16, 32)
                #Special case for level key
                if id == "k":
                    keys += 1
                #Ignore character if unknown 
                if id not in self.idtomod:
                    continue
                #Create object
                newobj = self.idtomod[id]((col*32)-32, (row*32)-32, 32, 32)
                #Add object to level's object list for computation 
                self.objects.append(newobj)
        
        #Set player needed keys
        self.chara.needed_keys = keys
        self.end()
        #Begin event loop 
        self.event_loop()

    def draw(self) -> None:
        """Special drawing method that preserves layering."""
        #In order of back to front: background, any game objects, player
        super().draw()
        self.bg.redraw()
        for obj in self.objects:
            obj.redraw()
        self.chara.redraw()

    def collision(self, player, obj) -> bool:
        """Receives an object and player and activates object collision method
on player. Returns collision result. Params: (player, obj)""" 
        return obj.collis(player)
   


    def event_loop(self) -> None:
        """Calculates all game events. This method is equivalent to 
1 gameplay frame. Handles collision order."""
        #Ask player to request new coordinates, or apply velocity before collision
        self.chara.move()
        #Sort objects by distance from player        
        self.objects.sort(key=lambda a: self.chara.cdist(a.Center()))
        #Start a counter - we only check the 12 closest objects to same time
        counter = 0
        #Run through objects 9not including player)
        for ind, obj in enumerate(self.objects):
            
            #Collide player and object
            a = self.collision(self.chara, obj)
            #Check if player has reached exit
            if isinstance(obj, exitportal) and a:
                #Check if player has needed amount of keys 
                if self.chara.keys >= self.chara.needed_keys:
                    #End level and exit function without scheduling next frame
                    self.endfunc()
                    return None
            #Key collision special case
            elif isinstance(obj, chest_key) and a:
                #delete key
                Fl.delete_widget(obj)
                #remove null ptr
                self.objects.pop(ind)
            #Object optimization counter increase 
            counter += 1
            #Optimization  
            if counter >= 12:
                break
        #Update and redraw player 
        self.chara.refresh()
        #Schedule next frame, attempting a bit over 60 fps 
        Fl.repeat_timeout(0.015, self.event_loop)

    
class Framework(Fl_Double_Window):
    """Constructor (None) - This is the general game class, which handles 
graphics, running the game, and the event loop."""

    def __init__(self, title = "Simple Platformer") -> None:
        """Constructor - Initialize window drawing and preparation"""

        Fl_Double_Window.__init__(self, 512, 768, title)
        #Level state, level variables 
        self.state = 0
        self.level = None
        #Load levels from text file 
        self.levels = open("levels.txt", "r").read().replace("\n", "").split("EL")
        #Store level dimensions 
        self.dim = [(16, 16), (16, 16), (16, 24), (10, 10), (16, 10), (16, 16)]
        #Begin timeline 
        self.timeline()
        #FLTK level display functions 
        self.show()
        Fl.run()

        
    def timeline(self) -> None:
        """Advances level."""
        #Avoid deleting level which doesn't exist
        if self.level:
            #Remove any running game loop
            Fl.remove_timeout(self.level.event_loop)
            #Delete currently loaded level 
            Fl.delete_widget(self.level)
        #Get level dimensions 
        s = self.dim[self.state]
        #Begin drawing 
        self.begin()
        #Create level
        self.level = Level(s[0]+2, s[1]+2, self.levels[self.state], "background1.jpg", self.timeline)
        #Resize level 
        self.resize(self.x(), self.y(), s[1]*32, s[0]*32)
        self.state += 1
            

#Start program
m = Framework()
