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
        
        

    def collis(self, pl):
        """Base collison method that checks for player hitbox->object hitbox intersection.
        Inherited by all game objects."""
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()
        plx, ply = pl.Px, pl.Py
        plx2, ply2 = plx+pl.w(), ply+pl.h()

        if ply2<sy or ply>sy2 or plx2<sx or plx>sx2:
            return False

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
        
        
    def collis(self, pl):
        '''Recieves a player object,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.h()

        isCol = super().collis(pl)
        if isCol:
            
            if pl.y()+pl.h()<=sy:
                #print("splat")
                pl.Py = min(pl.Py, (sy-pl.h())-1)
                pl.states["S"]=True
                return True
            if pl.y()>=sy2:
                #print("bonk")
                pl.Py=max(pl.Py, sy2+1)
                pl.states["N"]=True
                pl.yv = 0
                return True
        isCol = super().collis(pl)
        if isCol:
            if pl.x()>=sx2:
                #print("rightouchie")
                pl.Px = max(pl.Px, sx2+1)
                pl.states["W"]=True
                pl.xv = 0
                return True
            if pl.x()+pl.w()<=sx:
                #print("lefttouchie")
                pl.Px = min(pl.Px, (sx-pl.w())-1)
                pl.states["E"]=True
                pl.xv = 0
                return True
        return False
    

class Sawblade(Game_Object):

    '''Your standard, run of the mill stationary hazard.'''
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y, w, h, "sawblade.png")
        self.image(self.pic)

    def collis(self, pl):
        if super().collis(pl):
            pl.reset()

class exitportal(Game_Object):
    
    '''THe exit chest that allows you to progress to the next level.'''
    def __init__(self, x, y, w, h):
        '''initialize object'''
        Game_Object.__init__(self, x, y, w, h, "treasurechest.png")
        self.image(self.pic)
        self.nextlevelflag = False

    def collis(self, pl):
        '''exit collision detection, assuming the parent to
        this object will always be a game class'''
        a = super().collis(pl)


