
from fltk import *
from globs import *
from GameWidget import *


class Level(Fl_Group):
    """Level class that controls drawing and scheduling events for objects."""
    def __init__(self, r, c, s, bg, endfunc):
        #
        Fl_Group.__init__(self, 0, 0, 32*(c-2), 32*(r-2))
        self.objects = []
        self.chara = None
        self.idtomod = {
            "X": Solid_Block,
            "^": Sawblade,
            "*": exitportal,
            "=": jumppad,
            "k": chest_key
            }
        self.endfunc = endfunc

        self.begin()
        self.bg = Fl_Box(0, 0, 32*(c-2), 32*(r-2))
        self.bg.image(Fl_JPEG_Image(os.path.join(ASSETS, bg)).copy(self.bg.w(), self.bg.h()))
        
        keys = 0
        for row in range(r):
            for col in range(c):
                
                id = s[(row*c)+col]
                if id == "@":
                    self.chara = player((col*32)-32, (row*32)-32, 16, 32)

                if id == "k":
                    keys += 1
                if id not in self.idtomod:
                    continue
                newobj = self.idtomod[id]((col*32)-32, (row*32)-32, 32, 32)
                self.objects.append(newobj)

        self.chara.needed_keys = keys
        self.end()
        self.event_loop()

    def draw(self):
        super().draw()
        self.bg.redraw()
        for obj in self.objects:
            obj.redraw()
        self.chara.redraw()

    def collision(self, player, obj):
        
        return obj.collis(player)
   


    def event_loop(self):
        self.chara.move()
        self.objects.sort(key=lambda a: self.chara.cdist(a.Center()))
        counter = 0
        for ind, obj in enumerate(self.objects):
            
            a = self.collision(self.chara, obj)
            if isinstance(obj, exitportal) and a:
                if self.chara.keys >= self.chara.needed_keys:
                    self.endfunc()
                    return None
            elif isinstance(obj, chest_key) and a:
                Fl.delete_widget(obj)
                self.objects.pop(ind)
            counter += 1
            if counter >= 12:
                break
        self.chara.refresh()
        Fl.repeat_timeout(0.015, self.event_loop)

    
class Framework(Fl_Double_Window):
    '''This is the general game class, which handles 
    graphics, running the game, and the event loop.'''

    def __init__(self, title = "Simple Platformer"):
        """Initialize window drawing and preparation"""

        Fl_Double_Window.__init__(self, 512, 768, title)
        self.state = 2
        self.level = None
        #load levels from text file
        
        self.levels = open("levels.txt", "r").read().replace("\n", "").split("EL")
        self.dim = [(16, 16), (16, 16), (16, 24), (16, 16)]
        self.timeline()
        self.show()
        Fl.run()

        
    def timeline(self):
        #print(self.levels[self.state] == self.bruh[self.state])
        if self.level:
            Fl.remove_timeout(self.level.event_loop)
            Fl.delete_widget(self.level)
              
        s = self.dim[self.state]
        self.begin()
        self.level = Level(s[0]+2, s[1]+2, self.levels[self.state], "background1.jpg", self.timeline)
        self.resize(self.x(), self.y(), s[1]*32, s[0]*32)
        self.state += 1
            


m = Framework()
