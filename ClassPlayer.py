from fltk import *
from GameWidget import *
class player(Fl_Box):
    '''Initializes the player character and controls movement and graphics for it. Player is 16x * 32y.'''

    def __init__(self, x, y, w, h):
        '''Standard initializer giving values for xpos, ypos, while setting 
        gravity, xvelocity and yvelocity (g, xv, yv) to 0.'''
        Fl_Box.__init__(self, x, y, w, h)
        self.sprite = Fl_PNG_Image("tomatoboy.png")
        self.image(self.sprite.copy(w, h))

        self.g = 0.6
        self.xv = 0
        self.yv = 0
        self.Px = x
        self.Py = y
        self.airres = 0.1
        self.states = dict((ch, False) for ch in "NESW")
        self.keys = []
             
    def move(self):

        
        self.yv += self.g
        self.Px += self.xv
        self.Py += self.yv
        if self.xv != 0:
                print((self.xv/abs(self.xv))*min(self.airres, abs(self.xv)))
                self.xv -= (self.xv/abs(self.xv))*min(self.airres, abs(self.xv))

        return True
    
    def refresh(self):
        self.position(int(self.Px), int(self.Py))
        self.parent().redraw()
        

    def handle(self, event):
        r = 0

        if Fl.get_key(ord("A")):
            self.xv = max(-5, self.xv-1.5)
            r = 1

        if Fl.get_key(ord("D")):
            self.xv = min(5, self.xv+1.5)
            r = 1
    
        if Fl.get_key(ord("W")):
            if self.y()+self.h()>=self.parent().h():
                self.yv = -12
            r = 1
       
        return r
            
    #death function: do something upon death (in this case, reset to original pos)
    def reset(self):
        self.intx = self.originx
        self.inty = self.originy
        print("NOO")
    