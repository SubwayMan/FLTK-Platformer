
from fltk import *
from GameWidget import *
from ClassPlayer import *
from time import sleep
class Game(Fl_Window):
    '''This is the general game class, which handles 
    graphics, running the game, and the event loop.'''

    #standard textmap of each level
    

    def __init__(self, w, h, title = "Simple Platformer"):
        '''init'''
        Fl_Window.__init__(self, w, h, title)
        self.clevel = -1
        self.obj_arr = []
        self.show()
        self.background = Fl_JPEG_Image("background1.jpg")
        self.gamer = None
        self.levels = [(""
            "XXXXXXXXXXXXXXXXXX"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X.............X..X"
            "X.........X...X..X"
            "X.@....XXXX...X..X"
            "XXXXXXXXXXXXXXXXXX"
            "XXXXXXXXXXXXXXXXXX"
            ""), 
            (""
            "XXXXXXXXXXXXXXXXXX"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "X................X"
            "XXXXXXXXXXXXXXXXXX"
            "")]
         

    def drawcanvas(self, level, p_x, p_y):
        '''This is the function that draws each frame. it is responsible for loading 
        each level, drawing and creating all objects and calling the player's movement.'''
        self.begin()
        
        #special initialization for if the level changes
        if self.clevel != level:
            #empty array of objects (assuming python gc is automatic?)
            self.obj_arr = []
            #set current level
            self.clevel = level
            #load level, manage background, init variables for player pos
            iter = 0
            newmap = self.levels[self.clevel]
            bg = Fl_Box(0, 0, 512, 512)
            bg.image(self.background)
            px, py = 0, 0
            #goes tile by tile through canvas (16x16 grid) and creates objects
            for i in range(-32, 513, 32):
                for j in range(-32, 513, 32):
                    #load value for tile
                    tile = newmap[iter]
                    #block
                    if tile == "X":
                        newob = Solid_Block(j, i, 32, 32)
                        #objects are inserted in a specific order to get drawn.
                        #in order [background, static objects, mobiles, player]
                        self.obj_arr.insert(0, newob)

                    #player
                    if tile == "@":
                        px, py = j, i

                    iter += 1
            self.obj_arr.insert(0, bg)
     
            #create player
            self.gamer = player(px, py, self.obj_arr[1:])
            self.obj_arr.append(self.gamer)

        else:
            self.gamer.move()
            for obj in self.obj_arr:
                obj.redraw()
            
        
        self.end()

game = Game(512, 512)

game.drawcanvas(0, -32, -32)
state = Fl.wait()
while state:
    state = Fl.wait()
    game.drawcanvas(0, -32, -32)
    sleep(0.033)