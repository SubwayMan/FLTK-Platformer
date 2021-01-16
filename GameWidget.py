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
        plx, ply = pl.x(), pl.y()
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
        
        
    def collis(self, pl, X, X0):
        '''Recieves a player object,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
        
        
        
    

    

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


