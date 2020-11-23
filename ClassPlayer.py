from fltk import *
from GameWidget import *
class player(Fl_Box):
    '''Initializes the player character and controls movement and graphics for it. Player is 16x * 32y.'''

    def __init__(self, x, y, c_objects):
        '''Standard initializer giving values for xpos, ypos, while setting 
        gravity, xvelocity and yvelocity (g, xv, yv) to 0.'''
        Fl_Box.__init__(self, x, y, 16, 32)
        self.sprite = Fl_PNG_Image("tomatoboy.png")
        self.image(self.sprite)
        self.intx = x
        self.inty = y
        self.intw = 16
        self.inth = 32
        self.g = 0.7
        self.xv = 0
        self.yv = 0
        self.c_objects = c_objects
        self.STANDING_CHECK = True
        

    def collision(self, obj_arr):
        '''Given a list of objects currently in play, check if player is colliding with it. 
        obj_arr is a list of tuples, each tuple in the format (x, y, width, height). Hitboxes are rectangular.'''
        #TODO - more efficient collision algorithm

        #create list of dimension tuples to pass to player
        dtuples = []
        for obj in obj_arr:
            tempx, tempy, tempw, temph = obj.get_x(), obj.get_y(), obj.get_w(), obj.get_h()
            dtuples.append((tempx, tempy, tempw, temph))

        for pos, dtuple in enumerate(dtuples):
           
            obj_x, obj_y, obj_w, obj_h = dtuple
            directiondict = {}
            #check feet
            if (not ((self.intx < obj_x and self.intx + self.intw < obj_x) or \
                (self.intx > obj_x + obj_w and (self.intx + self.intw) > obj_x + obj_w))) and \
                self.inty + self.inth >= obj_y and self.inty + self.inth < (obj_y + obj_h):
     
                directiondict["PLAYER_BOTTOM"] = abs((self.inty+ self.inth) - obj_y)
                #obj_arr[pos].collis(self, "PLAYER_BOTTOM")
                #continue
            #check head
            if (not ((self.intx < obj_x and self.intx + self.intw < obj_x) or \
                (self.intx > obj_x + obj_w and (self.intx + self.intw) > obj_x + obj_w))) and \
                self.inty <= (obj_y+obj_h) and self.inty > (obj_y):
                
                directiondict["PLAYER_TOP"] = abs((obj_y + obj_h) - self.inty)
                #obj_arr[pos].collis(self, "PLAYER_TOP")
            #check right side
            if (not ((self.inty < obj_y and self.inty + self.inth < obj_y) or \
                (self.inty > obj_y + obj_h and (self.inty + self.inth) > obj_y + obj_h))) and \
                self.intx + self.intw >= obj_x and self.intx + self.intw < (obj_x+obj_w):

                directiondict["PLAYER_RIGHT"] = abs((self.intx + self.intw) - obj_x)
                #obj_arr[pos].collis(self, "PLAYER_RIGHT")

            #check left side
            if (not ((self.inty < obj_y and self.inty + self.inth < obj_y) or \
                (self.inty > obj_y + obj_h and (self.inty + self.inth) > obj_y + obj_h))) and \
                self.intx <= (obj_x+obj_w) and self.intx > (obj_x):
                
                directiondict["PLAYER_LEFT"] = abs((obj_x + obj_w) - self.intx)
            
            if directiondict:
                dec = min(directiondict, key = lambda a: directiondict[a])
                obj_arr[pos].collis(self, dec)
            
    def move(self):
        
        self.inty += self.yv
        self.STANDING_CHECK = False
        self.collision(self.c_objects)
        if self.STANDING_CHECK:
            self.yv = 0
        self.intx += self.xv

        self.position(self.intx, int(self.inty))
        self.xv = 0
        if not self.STANDING_CHECK:
            self.yv += self.g

    def handle(self, event):
        n = False
        if Fl.event_key(FL_Up):
            if self.STANDING_CHECK:
                self.yv = -12
            n = True
                
        if Fl.event_key(FL_Right):
            self.xv = 5
            n = True
           
        if Fl.event_key(FL_Down):
            self.yv = 3
            n = True
           
        if Fl.event_key(FL_Left):
            self.xv = -5
            n = True
        return 1 if n else 0
            

    #getter and setter methods
    def get_x(self):
        return self.intx
    
    def get_y(self):
        return self.inty

    def get_xv(self):
        return self.xv

    def get_yv(self):
        return self.yv

    def get_w(self):
        return self.intw

    def get_h(self):
        return self.inth

    def get_g(self):
        return self.STANDING_CHECK

    def set_x(self, n):
        self.intx = n
    
    def set_y(self, n):
        self.inty = n

    def set_xv(self, n):
        self.xv = n

    def set_yv(self, n):
        self.yv = n

    def grav(self):
        self.STANDING_CHECK = True
