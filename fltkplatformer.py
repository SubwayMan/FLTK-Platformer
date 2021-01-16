
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
        self.chara = None
        self.idtomod = {
            "X": Solid_Block,
            "^": Sawblade,
            }

        self.begin()
        self.bg = Fl_Box(0, 0, 32*(c-2), 32*(r-2))
        self.bg.image(Fl_JPEG_Image(bg).copy(self.bg.w(), self.bg.h()))
        
        for row in range(r):
            for col in range(c):
                
                id = s[(row*c)+col]
                if id == "@":
                    self.chara = player((col*32)-32, (row*32)-32, 16, 32)

                if id not in self.idtomod:
                    continue
                newobj = self.idtomod[id]((col*32)-32, (row*32)-32, 32, 32)
                self.objects.append(newobj)
        self.end()
        self.event_loop()

    def draw(self):
        super().draw()
        self.bg.redraw()
        for obj in self.objects:
            obj.redraw()
        self.chara.redraw()

    def collision(self, player, obj):
        
        
        if player.Py > self.h()-player.h():
            player.Py = self.h()-player.h()
            player.states["S"] = True

        
        obj.collis(player)


    def event_loop(self):
        self.chara.move()
        for obj in self.objects:
            self.collision(self.chara, obj)
        self.chara.refresh()
        Fl.repeat_timeout(0.015, self.event_loop)

    
class Framework(Fl_Double_Window):
    '''This is the general game class, which handles 
    graphics, running the game, and the event loop.'''

    def __init__(self, title = "Simple Platformer"):
        """Initialize window drawing and preparation"""

        Fl_Double_Window.__init__(self, 512, 768, title)
        self.state = 1
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
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            ".........................."
            "...@........^^....^......."
            ".........................."
            ""),
            (""
            "XXXXXXXXXXXXXXXXXXXXXXXXXX"
            "X........................X"
            "X........XXX.............X"
            "X.............XX.^.XX....X"
            "X...............^.^.....^X"
            "X..XX^...........^.......X"
            "X.......XXX..............X"
            "X.............X.........XX"
            "X.............X.......X^.X"
            "X.............X..........X"
            "X.....X^...XX^X..........X"
            "X.X........^.............X"
            "X..........^.............X"
            "X....XXX...X.............X"
            "X..........X.............X"
            "X..........X.............X"
            "X..X..XXX^^X.............X"
            "XXXXXXXXXXXXXXXXXXXXXXXXXX"
            "")]

        self.dim = [(16, 16), (16, 24)]
        self.timeline()
        self.show()
        Fl.run()

        
    def timeline(self):
        if self.level:
            Fl.remove_timeout(self.level.event_loop)
            Fl.delete_widget(self.level)
              
        s = self.dim[self.state]
        self.begin()
        self.level = Level(s[0]+2, s[1]+2, self.levels[self.state], "background1.jpg")
        self.resize(self.x(), self.y(), s[1]*32, s[0]*32)
        self.state += 1
            


m = Framework()