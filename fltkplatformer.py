
from fltk import *
from GameWidget import *
#from ClassPlayer import *
from time import sleep

class Level(Fl_Group):
    """Level class that controls drawing and scheduling events for objects."""
    def __init__(self, r, c, s, bg):
        #
        Fl_Group.__init__(self, 0, 0, 32*(c-2), 32*(r-2))
        self.objects = []
        self.idtomod = {
            "X": Solid_Block,
            "@": Sawblade
            }
        self.bg = Fl_Box(0, 0, 32*(c-2), 32*(r-2))
        self.bg.image(Fl_JPEG_Image(bg).copy(self.bg.w(), self.bg.h()))
        self.begin()

        for row in range(r):
            for col in range(c):
                print((row*r)+c)
                id = s[(row*r)+c]
                if id not in self.idtomod:
                    continue
                newobj = self.idtomod[id]((r*32)-32, (c*32)-32, 32, 32)
                self.objects.append(newobj)
        self.end()


class Framework(Fl_Double_Window):
    '''This is the general game class, which handles 
    graphics, running the game, and the event loop.'''

    def __init__(self, title = "Simple Platformer"):
        """Initialize window drawing and preparation"""

        Fl_Double_Window.__init__(self, 512, 768, title)
        self.state = 0
        self.level = None
        #standard textmap of each level
        self.levels = [(""
            "XXXXXXXXXXXXXXXXXX"
            "X................X"
            "XXXXX............X"
            "X........X.......X"
            "X........X.......X"
            "X.....X^^X......*X"
            "X.....X......XXXXX"
            "X..X^^X..........X"
            "X..X.............X"
            "X................X"
            "XX......X^X......X"
            "XXXXXXXXXXXX.....X"
            "X................X"
            "X.............X..X"
            "X.........X...X..X"
            "X.@....X^^X...X..X"
            "XXXXXXXXXXXXXXXXXX"
            "XXXXXXXXXXXXXXXXXX"
            ""), 
            (""
            "XXXXXXXXXXXXXXXXXXXXXXXXXX"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "X........................X"
            "XXXXXXXXXXXXXXXXXXXXXXXXXX"
            "")]
        self.dim = [(16, 16), (16, 24)]
        self.timeline()
        self.show()
        Fl.run()
        
    def timeline(self):
        if self.level:
            Fl.delete_widget(self.level)
              
        s = self.dim[self.state]
        self.begin()
        self.level = Level(s[0]+2, s[1]+2, self.levels[self.state], "background1.jpg")
        self.state += 1
            


m = Framework()