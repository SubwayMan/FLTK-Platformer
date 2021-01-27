from fltk import *
from ClassPlayer import *
from globs import *
import os	
#---------------------------HEADER-----------------------------
#This file contains the classes for the game objects.
#This refers to static, non-user-controlled instances.
#Expected handling: Collision mechanics. Most objects will expect 
#a player class being passed in some form.
#All objects inherit default collision and basic image/graphic management.

class Game_Object(Fl_Box):
    """Parent class for all game objects. Handles drawing of all subclasses. Inheriting from blank
box method. Constructor args:
- x, y, w, h: dimensions,
- spr: sprite to pull from ASSETS directory.
"""
    def __init__(self, x, y, w, h, spr) -> None:
        """Constructor."""
        #initialize Fl_Box superclass
        Fl_Box.__init__(self, x, y, w, h)
        #Load the location of the sprite by pulling asset directory location from globals
        sprite = os.path.join(ASSETS, spr)
        #This is a debugging sprite that any game object can call/use
        self.debugsprite = Fl_PNG_Image(os.path.join(ASSETS, "debug.png"))
        #Now defunct legacy code for image management. Will switch to solely PNGs soon
        if sprite.endswith(".jpg"):
            self.pic = Fl_JPEG_Image(sprite)
        elif sprite.endswith(".png"):
            self.pic = Fl_PNG_Image(sprite)
        #Resize given image to widget bounding box
        self.image(self.pic.copy(w, h))
        
        

    def collis(self, pl) -> bool:
        """Base collison method that checks for player hitbox -> object hitbox intersection.
    Inherited by all game objects. Convention is for any collision method to return a 
    boolean value."""
        #Grab our point coordinates, in order NW, NE, SW, SE.
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()
        #See previous comment, but for the player's bounding box.
        plx, ply = pl.Px, pl.Py
        plx2, ply2 = plx+pl.w(), ply+pl.h()
        #Main collision check. Returns False if:
        #player east edge to west of self west edge,
        #player west edge to east of self east edge,
        #player south edge north of self north edge,
        #player north edge south of self south edge.
        if ply2<sy or ply>=sy2 or plx2<sx or plx>=sx2:
            return False
        #If all those checks fail, return a valid collision result.
        return True

    def Center(self)->(int, int):
        """A method that returns coordinates of center point, for
use in distance calculations."""
        a = self.x()+(self.w()//2)
        b = self.y()+(self.h()//2)
        return(a, b)


class Solid_Block(Game_Object):
    """Block game object, Main object for interaction between 
player and canvas, base of all platforming elements. Responsible for 
pushing back the player, and allowing player to jump/walljump."""
 
    def __init__(self, x, y, w, h) -> None:
        """Constructor. Sprite is already supplied, takes basic dimension arguments."""
        Game_Object.__init__(self, x, y, w, h, "platformblock.png")     
 
        
    def collis(self, pl) -> bool:
        """Special block specific block -> player collision method.
Alters inputted player's requested input depending on collision."""
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()

        isCol = super().collis(pl)
        if isCol:
            
            if pl.y()+pl.h()<=sy:

                pl.Py = min(pl.Py, (sy-pl.h()))
                pl.states["S"]=True
                return True
            if pl.y()>=sy2:

                pl.Py=max(pl.Py, sy2)
                pl.states["N"]=True
                pl.yv = 0
                return True
        isCol = super().collis(pl)
        
        if isCol:
            if pl.x()>=sx2:

                pl.Px = max(pl.Px, sx2)
                pl.states["W"]=True
                pl.xv = 0
                return True
            if pl.x()+pl.w()<=sx:
              
                pl.Px = min(pl.Px, (sx-pl.w())-1)
                pl.states["E"]=True
                pl.xv = 0
                return True
        return False
    


class Sawblade(Game_Object):

    '''Your standard, run of the mill stationary hazard.'''
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x+1, y+1, w-2, h-2, "sawblade.png")



    def collis(self, pl):
        if super().collis(pl):
            pl.reset()


class exitportal(Game_Object):
    
    '''THe exit chest that allows you to progress to the next level.'''
    def __init__(self, x, y, w, h):
        '''initialize object'''
        Game_Object.__init__(self, x, y, w, h, "treasurechest.png")




class jumppad(Game_Object):
    """A typical 'trampoline' element."""
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y+(h//2), w, h//2, "jumppad.png")


    def collis(self, pl):
        if super().collis(pl):
            pl.yv = -15
            pl.xv /= 5
            pl.Py -= 2

class chest_key(Game_Object):
    """Keys that enable or disable the chest that transports to the next level."""
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y, w, h, "key.png")


    def collis(self, pl):
        if super().collis(pl):
            pl.keys += 1
            return True
        return False


