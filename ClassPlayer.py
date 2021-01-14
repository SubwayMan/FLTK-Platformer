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

        self.g = 0.5
        self.Ox = x
        self.Oy = y
        self.reset()
        self.airres = 0.05
        self.friction = 0.2
        self.states = dict((ch, False) for ch in "NESW")
        self.keys = set()
             
    def move(self):

        fflag = False
        for k in self.states:
            self.states[k] = False

        if ord("a") in self.keys:
            self.xv = max(-4, self.xv-0.7)


        if ord("d") in self.keys:
            self.xv = min(4, self.xv+0.7)
        
        if self.y()+self.h()>=self.parent().h():
            if ord("w") in self.keys:
                self.yv = -10
            fflag = True

        self.yv = min(self.yv+self.g, 20)
        self.Px += self.xv
        self.Py += self.yv
   
        self.negwork(self.airres)

        if fflag:
            self.negwork(self.friction)
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
        if FL_KEYDOWN:
            self.keys.add(Fl.event_key())
            r = 1
        if FL_KEYUP:
            nset = set()
            for k in self.keys:
                if Fl.get_key(k):
                    nset.add(k)
            self.keys = nset
            r = 1
                 
       
        return r
    
    def reset(self):
        """death function: do something upon death (in this case, reset to original pos)"""
        self.position(self.Ox, self.Oy)
        self.xv = 0
        self.yv = 0
        self.Px = self.x()
        self.Py = self.y()

