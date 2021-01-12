from fltk import *
from ClassPlayer import *
class Game_Object(Fl_Box):
    '''parent class for all game objects.'''
    def __init__(self, x, y, w, h, sprite):
        '''typical init function'''
        Fl_Box.__init__(self, x, y, w, h)
        self.intx = x
        self.inty = y        
        self.intw = w
        self.inth = h
        self.debugsprite = Fl_PNG_Image("debug.png")
        if sprite.endswith(".jpg"):
            self.pic = Fl_JPEG_Image(sprite)
        elif sprite.endswith(".png"):
            self.pic = Fl_PNG_Image(sprite)
    
    def collis(self, pl, collis_t):
        '''Recieves a player object and direction of collision,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
        pass

    #getter and setter methods
    def get_x(self):
        return self.intx
    
    def get_y(self):
        return self.inty

     #getter and setter methods
    def get_w(self):
        return self.intw
    
    def get_h(self):
        return self.inth
    

class Solid_Block(Game_Object):
    '''Class for solid surfaces (walls, floors)'''
    #load sprite

    def __init__(self, x, y, w, h):
        '''typical init function'''
        Game_Object.__init__(self, x, y, w, h, "platformblock.jpg")     
        self.image(self.pic)
        #print(f"block created at {x}, {y}")
        
        
    def collis(self, pl, collis_t):
        print(collis_t)
        #self.image(self.debugsprite)
        if collis_t == "PLAYER_TOP": 
            pl.set_yv(0)
            pl.set_y(self.inty + self.inth)

        if collis_t == "PLAYER_BOTTOM":
            print(pl.get_g())
            pl.grav()
            plh = pl.get_h()
            #print(plh, self.inty)
            pl.set_y(self.inty - plh)
            
        if collis_t == "PLAYER_LEFT":
            pl.set_x(self.intx + self.intw)
            pl.set_xv(max(0, pl.get_xv()))
        if collis_t == "PLAYER_RIGHT":
            
            plw = pl.get_w()
            pl.set_x(self.intx - plw)
            pl.set_xv(min(0, pl.get_xv()))
        
        return False

     


class Sawblade(Game_Object):

    '''Your standard, run of the mill stationary hazard.'''
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y, w, h, "sawblade.png")
        self.image(self.pic)

    def collis(self, pl, collis_t):
        pl.reset()

class exitportal(Game_Object):
    
    '''THe exit chest that allows you to progress to the next level.'''
    def __init__(self, x, y, w, h):
        '''initialize object'''
        Game_Object.__init__(self, x, y, w, h, "debugsprite.jpg")
        self.image(self.debugsprite)
        self.nextlevelflag = False

    def collis(self, pl, collis_t):
        '''exit collision detection, assuming the parent to
        this object will always be a game class'''
        self.nextlevelflag = True 
    def getselfflag(self):
        '''return flag status for handling
        NOTE: method for setting nextlevelflag is not present. In theory,
        when nextlevelflag is TRUE, all objects will be deleted and replaced.'''
        return self.nextlevelflag


