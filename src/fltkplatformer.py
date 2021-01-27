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

class GUIbutton(Fl_Button):
    
    """Special button class with custom looks for GUI and navigation purposes.
Constructor: GUIbutton(x, y, w, h, label)"""
    
    def __init__(self, x, y, w, h, label=None) -> None:
        
        """Constructor."""
        #Call fltk button instance
        Fl_Button.__init__(self, x, y, w, h, label)
        self.upimg = Fl_PNG_Image(os.path.join(ASSETS, "upbutspr.png"))
        self.downimg = Fl_PNG_Image(os.path.join(ASSETS, "downbutspr.png"))
        self.image(self.upimg.copy(w, h))
        
    def handle(self, e) -> int:
        """Overriding handle method to manage its appearance
upon press/release."""
        #use FLTK's button handling
        a = super().handle(e)
        #Button "pops up" if mouse not over or mouse released
        if not a or e == FL_RELEASE:
            #set up image
            self.image(self.upimg.copy(self.w(), self.h()))
            #redraw button 
            self.redraw()
            return a
        #Push button otherwise
        self.image(self.downimg.copy(self.w(), self.h()))
        self.redraw()
        return a



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

        Fl_Double_Window.__init__(self, 512, 512, title)
        #Level state, level variables 
        self.state = 0
        self.level = None
        #Load levels from text file 
        self.levels = open("levels.txt", "r").read().split("\n\n")
        #Create background canvas
        self.bg = Fl_Box(0, 0, self.w(), self.h())
        #create button
        self.startbut = GUIbutton(200, 200, 108, 76, "PLAY")
        self.startbut.hide()
        #set callback
        self.startbut.callback(self.timeline)
        #Start screen 
        self.startscreen()
        #FLTK level display functions 
        self.show()
        Fl.run()

        
    def timeline(self, w=None) -> None:
        """Advances level."""
        #Avoid deleting level which doesn't exist
        if self.level:
            #Remove any running game loop
            Fl.remove_timeout(self.level.event_loop)
            #Delete currently loaded level 
            Fl.delete_widget(self.level)
        #disable button
        self.startbut.hide()
        self.startbut.deactivate()
        #Begin drawing 
        self.begin()
        #get level and dimensions
        nlevel = self.levels[self.state].split("\n")
        r = len(nlevel)
        c = len(nlevel[0])
        #Create level
        self.level = Level(r, c, "".join(nlevel) , "background1.jpg", self.timeline)
        #Resize level 
        self.resize(self.x(), self.y(), (c-2)*32, (r-2)*32)
        self.state += 1
            
    def startscreen(self) -> None:
        """Manager for the starting screen."""
        #reset level
        self.state=0
        #Set background        
        self.bg.image(Fl_JPEG_Image(os.path.join(ASSETS, "background1.jpg")).copy(self.bg.w(), self.bg.h()))
        #show start button
        self.startbut.show()
        self.startbut.redraw()

#Start program
m = Framework()
