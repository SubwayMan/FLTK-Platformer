from fltk import *
from ClassPlayer import *
class Game_Object(Fl_Box):
    '''defunct for now'''
    def __init__(self, x, y, w, h):
        '''typical init function'''
        self.x = x
        self.y = y
        self.w = w
        self.h = h
       
    
    def collis(self, pl, collis_t):
        '''Recieves a player object and direction of collision,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
    

class Solid_Block(Fl_Box):
    '''Class for solid surfaces (walls, floors)'''
    #load sprite

    def __init__(self, x, y, w, h):
        '''typical init function'''
        Fl_Box.__init__(self, x, y, w, h)
        self.pic = Fl_JPEG_Image("platformblock.jpg")
        self.image(self.pic)
        self.intx = x
        self.inty = y
        self.intw = w
        self.inth = h
        self.debugsprite = Fl_PNG_Image("debug.png")
        
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
