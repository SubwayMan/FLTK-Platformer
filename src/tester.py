
from fltk import *
#from GameWidget import *

class testclass(Fl_Button):
    def __init__(self, x, y, w, h):
        Fl_Button.__init__(self, x, y, w, h)

    def handle(self, e):
       
        if Fl.event_key(FL_Up):
            self.color(FL_GREEN)
            self.redraw()
            return 1
        if Fl.event_key(FL_Right):
            self.color(FL_RED)
            self.redraw()
            return 1
        if Fl.event_key(FL_Down):
            self.color(FL_BLUE)
            self.redraw()
            return 1
        if Fl.event_key(FL_Left):
            self.color(FL_YELLOW)
            self.redraw()
            return 1
        return 0
n = Fl_Window(500, 500)
n.begin()
cccc = testclass(0, 0, 50, 50)
p = Fl_Button(20, 0, 50, 50)
k = Fl_Button(50, 0, 50, 50)
n.end()
n.show()
Fl.run()
