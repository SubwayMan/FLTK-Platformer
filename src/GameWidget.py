from fltk import *
from ClassPlayer import *
from globs import *
import os	
class Game_Object(Fl_Box):
    '''parent class for all game objects.'''
    def __init__(self, x, y, w, h, spr):
        '''typical init function'''
        Fl_Box.__init__(self, x, y, w, h)
        sprite = os.path.join(ASSETS, spr)
        self.debugsprite = Fl_PNG_Image(os.path.join(ASSETS, "debug.png"))
        if sprite.endswith(".jpg"):
            self.pic = Fl_JPEG_Image(sprite)
        elif sprite.endswith(".png"):
            self.pic = Fl_PNG_Image(sprite)
        self.image(self.pic.copy(w, h))
        
        

    def collis(self, pl):
        """Base collison method that checks for player hitbox->object hitbox intersection.
        Inherited by all game objects."""
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()
        plx, ply = pl.Px, pl.Py
        plx2, ply2 = plx+pl.w(), ply+pl.h()

        if ply2<sy or ply>=sy2 or plx2<sx or plx>=sx2:
            return False
        return True

    def Center(self)->(int, int):
        """A method that returns coordinates of center point, for use in distance calculations."""
        a = self.x()+(self.w()//2)
        b = self.y()+(self.h()//2)
        return(a, b)


class Solid_Block(Game_Object):
    '''Class for solid surfaces (walls, floors)'''
    #load sprite

    def __init__(self, x, y, w, h):
        '''typical init function'''
        Game_Object.__init__(self, x, y, w, h, "platformblock.jpg")     
 
        #print(f"block created at {x}, {y}")
        self.reflect = dict((f, g) for f, g in zip("NESW", "SWNE"))
        #a face is represented by its type, its lower bound, its upper bound, and its plane location
        #ex. a face ("HOR", 10, 20, 60) is a horizontal surface from x10->20 located at y 60
        self.faces = {
            "N": (x, x+w, y),
            "S": (x, x+w, y+h),
            "W": (y, y+h, x),
            "E": (y, y+h, x+w),
            }
        
        
    def collis(self, pl):
        '''Recieves a player object,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
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

                pl.Px = max(pl.Px, sx2+1)
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
        Game_Object.__init__(self, x, y, w, h, "sawblade.png")



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
        Game_Object.__init__(self, x, y+(h//2), w, h//2, "key.png")


    def collis(self, pl):
        if super().collis(pl):
            pl.keys += 1
            return True
        return False
