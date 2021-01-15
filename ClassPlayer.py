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
        self.Ox = x
        self.Oy = y
        self.reset()
        self.airres = 0.05
        self.friction = 0.4
        self.states = dict((ch, False) for ch in "NESW")
        self.jump = True
        Fl.focus(self)
             
    def move(self):

        fflag = False
        self.yv = min(self.yv+self.g, 20)

        if Fl.get_key(FL_Left):
            self.xv = max(-4, self.xv-0.7)


        if Fl.get_key(FL_Right):
            self.xv = min(4, self.xv+0.7)
        
        if self.states["S"]:
            self.yv = 0
            
            self.negwork(self.friction)

        if Fl.get_key(ord("c")):
            if self.jump and self.states["S"]:
                self.yv = -11
                self.jump = False

        if self.xv == 0 and self.yv == 0:
            return False

        self.Px += self.xv
        self.Py += self.yv
        
        self.negwork(self.airres)
        
            

        for k in self.states:
            self.states[k] = False
        return True
    
    def refresh(self):
        self.position(int(self.Px), int(self.Py))
        self.parent().redraw()
        
    def negwork(self, n):
        if self.xv == 0:
            return None
        self.xv -= (self.xv/abs(self.xv))*min(n, abs(self.xv))
      
    def handle(self, event):
        r = 0
        super().handle(event)
        if event == FL_KEYUP:
            if Fl.event_key() == ord("c"):
                self.jump = True
                r = 1

        return r
    
    def reset(self):
        """death function: do something upon death (in this case, reset to original pos)"""
        self.position(self.Ox, self.Oy)
        self.xv = 0
        self.yv = 0
        self.Px = self.x()
        self.Py = self.y()

