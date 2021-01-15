from fltk import *
from ClassPlayer import *
class Game_Object(Fl_Box):
    '''parent class for all game objects.'''
    def __init__(self, x, y, w, h, sprite):
        '''typical init function'''
        Fl_Box.__init__(self, x, y, w, h)
        self.debugsprite = Fl_PNG_Image("debug.png")
        if sprite.endswith(".jpg"):
            self.pic = Fl_JPEG_Image(sprite)
        elif sprite.endswith(".png"):
            self.pic = Fl_PNG_Image(sprite)
        
        

    def collis(self, pl, X, X0):
        """Base collison method that checks for player hitbox->object hitbox intersection.
        Inherited by all game objects."""
        for p in X:
            if self.x()<=p[0]<=self.x()+self.w() and self.y()<=p[1]<=self.y()+self.h():
                return True


                

class Solid_Block(Game_Object):
    '''Class for solid surfaces (walls, floors)'''
    #load sprite

    def __init__(self, x, y, w, h):
        '''typical init function'''
        Game_Object.__init__(self, x, y, w, h, "platformblock.jpg")     
        self.image(self.pic)
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
        
        
    def collis(self, pl, X, X0):
        '''Recieves a player object,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
        
        dx = int(pl.Px - pl.x())
        dy = int(pl.Py - pl.y())
        if dx == 0 and dy == 0:
            return None
        plfacedict = {
            "N": (X[0], X[1]),
            "S": (X[2], X[3]),
            "E": (X[1], X[3]),
            "W": (X[0], X[2])
            }

        coltype = ""
        if dx>0:
            coltype += "W"
        elif dx < 0:
            coltype += "E"
        if dy>0:
            coltype += "N"
        elif dy < 0:
            coltype += "S"
        if not coltype:
            return False
        #print(coltype)
        for ch in coltype:

            ans = self.face_push(pl, plfacedict[self.reflect[ch]], ch)
            if ans == None:
                continue
            self.modify(pl, ch, ans)
            
        
    def face_push(self, pl, edge, id):
        """Helper function for collision."""
        if super().collis(pl, edge, []):
            if id == "N":
                return self.y()+self.h()
            elif id == "S":
                return self.y()-pl.h()
            elif id == "W":
                return self.x()-pl.w()
            elif id == "E":
                return self.x()+self.w()+1
      
        return None

    def modify(self, pl, ch, val):
        """Another helper function designed to avoid repetition on face priority calculations."""
        pl.states[ch] = True
        if ch in "NS":
            pl.Py = val
            pl.yv = 0
        elif ch in "EW":
            pl.Px = val
            pl.xv = 0


class Sawblade(Game_Object):

    '''Your standard, run of the mill stationary hazard.'''
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y, w, h, "sawblade.png")
        self.image(self.pic)

    def collis(self, pl, X, X0):
        if super().collis(pl, X, X0):
            pl.reset()

class exitportal(Game_Object):
    
    '''THe exit chest that allows you to progress to the next level.'''
    def __init__(self, x, y, w, h):
        '''initialize object'''
        Game_Object.__init__(self, x, y, w, h, "treasurechest.png")
        self.image(self.pic)
        self.nextlevelflag = False

    def collis(self, pl, X, X0):
        '''exit collision detection, assuming the parent to
        this object will always be a game class'''
        a = super().collis(pl, X, X0)


