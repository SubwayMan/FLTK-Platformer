from fltk import *
from globals import *
import math
class player(Fl_Box):
    '''Initializes the player character and controls movement and graphics for it. Player is 16x * 32y.'''

    def __init__(self, x, y, w, h):
        '''Standard initializer giving values for xpos, ypos, while setting 
        gravity, xvelocity and yvelocity (g, xv, yv) to 0.'''
        Fl_Box.__init__(self, x, y, w, h)
        self.sprite = Fl_PNG_Image(os.path.join(ASSETS, "tomatoboy.png"))
        self.image(self.sprite.copy(w, h))


        self.g = 0.6

        self.Ox = x
        self.Oy = y
        self.reset()
        self.airres = 0.05

        self.friction = 0.8
        self.appliedxv = 0.4
        self.states = dict((ch, False) for ch in "NESW")
        self.jump = True
        Fl.focus(self)
             
    def move(self):

        fflag = False

        if Fl.get_key(FL_Left):
            self.xv = max(-4, self.xv-self.appliedxv)

        elif Fl.get_key(FL_Right):

            self.xv = min(4, self.xv+self.appliedxv)
        else:
            if self.states["S"]:
                fflag = True
        
        if not self.states["S"]:
            
            self.yv = min(self.yv+self.g, 16)
        else:
            if not self.appliedxv:
                self.enable_inp()
                Fl.remove_timeout(self.enable_inp)
            self.yv = 1


        if Fl.get_key(ord("c")):
          
            if self.jump and self.states["S"]:
                self.yv = -11
                self.jump = False
            elif self.jump and self.states["E"]:
                self.yv = -9
                self.xv = -5
                self.jump = False
                self.appliedxv = 0
                Fl.repeat_timeout(0.2, self.enable_inp)
            elif self.jump and self.states["W"]:
                self.yv = -9
                self.xv = 5
                self.jump = False
                self.appliedxv = 0
                Fl.repeat_timeout(0.2, self.enable_inp)

        if self.xv == 0 and self.yv == 0:
            return False

        self.Px += self.xv
        self.Py += self.yv
        
        self.negwork(self.airres)
        if fflag:
            self.negwork(self.friction)
            

        for k in "NS":
            self.states[k] = False
        if int(self.Px)!=self.x():
            self.states["E"] = False
            self.states["W"] = False

    
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
    
    def cdist(self, coords) -> bool:
        """Returns the distance between a point and player center, for use in collision calcs"""
        xp = self.x()+(self.w()//2)
        yp = self.y()+(self.w()//2)
        return math.sqrt(math.pow(coords[0]-xp, 2)+math.pow(coords[1]-yp, 2))

    def reset(self):

        """death function: do something upon death (in this case, reset to original pos)"""

        self.position(self.Ox, self.Oy)
        self.xv = 0
        self.yv = 0
        self.Px = self.x()
        self.Py = self.y()

    def enable_inp(self):
        self.appliedxv = 0.4


