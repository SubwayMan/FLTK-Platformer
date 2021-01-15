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
        
        Nx, Ny = pl.Px, pl.Py

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
            a = self.face_push(pl, pl.x(), pl.y(), ch)
            print(ch, a)
            if a:
                return True
        return False
            
        
    def face_push(self, pl, fx, fy, id):
        """Helper function for collision."""
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()
        if id == "N":
            if not ((fx<sx and fx+pl.w()<sx) or (fx>sx2 and fx+pl.w()>sx2)):
                if pl.Py+pl.h()>=sy:
                    pl.Py = (sy-pl.h())-1
                    return True
            
        elif id == "S":
            if not ((fx<sx and fx+pl.w()<sx) or (fx>sx2 and fx+pl.w()>sx2)):
                if pl.Py<=sy2:
                    pl.Py = sy2+1
                    return True
        elif id == "E":
            if not ((fy<sy and fy+pl.h()<sy) or (fy>sy2 and fy+pl.h()>sy2)):
                if pl.Px<=sx2:
                    pl.Px = sx2+1
                    return True
        elif id == "W":
            if not ((fy<sy and fy+pl.h()<sy) or (fy>sy2 and fy+pl.h()>sy2)):
                if pl.Px+pl.w()>=sx:
                    pl.Px = (sx-pl.w())-1
                    return True
      
        return False

    

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


