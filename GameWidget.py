from fltk import *
from ClassPlayer import *
class Game_Object(Fl_Box):
    '''parent class for all game objects.'''
    def __init__(self, x, y, w, h, sprite):
        '''typical init function'''
        Fl_Box.__init__(self, x, y, w, h)
        self.intx = x
        self.inty = y        
        self.intw = w
        self.inth = h
        self.debugsprite = Fl_PNG_Image("debug.png")
        if sprite.endswith(".jpg"):
            self.pic = Fl_JPEG_Image(sprite)
        elif sprite.endswith(".png"):
            self.pic = Fl_PNG_Image(sprite)
        
        self.reflect = dict((f, g) for f, g in zip("NESW", "SWNE"))
        #a face is represented by its type, its lower bound, its upper bound, and its plane location
        #ex. a face ("HOR", 10, 20, 60) is a horizontal surface from x10->20 located at y 60
        self.faces = {
            "N": ("HOR", x, x+w, y),
            "S": ("HOR", x, x+w, y+h),
            "W": ("VERT", y, y+h, x),
            "E": ("VERT", y, y+h, x+w),
            }

    def collis(self, pl, X, X0):
        '''Recieves a player object,
        then changes player's attributes accordingly. This method has to 
        be reimplemented throughout all game objects.'''
        if not super().collis():
            return False

        sx, sy = self.x(), self.y()
        sx2, sy2 = sx+self.w(), sy+self.y()

        for point in X0:
            if sx<point[0]<sx2 and sy<point[1]<sy2:
                return True
        return False

    def VectorFaceIntersect(self, vec, face) -> bool:

        p1, p2 = vec
        Dy = p2[1]-p1[1]
        Dx = p2[0]-p1[0]
        if face[0] == "HOR":
            
            if (p1[0]<face[1] and p2[0]<face[1]) or (p1[0]>face[2] and p2[0]>face[2]):
                return None

            nDy = face[3]-p1[1]
            nDx = Dx*(nDy/Dy)
            if face[1]<p1[0]+nDx<face[2]:
                return True
            
        if face[0] == "VERT":

            if (p1[1]<face[1] and p2[1]<face[1]) or (p1[1]>face[2] and p2[1]>face[2]):
                return None

            nDx = face[3]-p1[0]
            nDy = Dy*(nDx/Dx)
            if face[1]<p1[1]+nDy<face[2]:
                return True
                

class Solid_Block(Game_Object):
    '''Class for solid surfaces (walls, floors)'''
    #load sprite

    def __init__(self, x, y, w, h):
        '''typical init function'''
        Game_Object.__init__(self, x, y, w, h, "platformblock.jpg")     
        self.image(self.pic)
        #print(f"block created at {x}, {y}")
        
        
    def collis(self, pl, X, X0):
        pass

     


class Sawblade(Game_Object):

    '''Your standard, run of the mill stationary hazard.'''
    def __init__(self, x, y, w, h):
        Game_Object.__init__(self, x, y, w, h, "sawblade.png")
        self.image(self.pic)

    def collis(self, pl, X, X0):
        if super().collis(pl, X, X0):
            pl.reset()

class exitportal(Game_Object):
    
    '''THe exit chest that allows you to progress to the next level.'''
    def __init__(self, x, y, w, h):
        '''initialize object'''
        Game_Object.__init__(self, x, y, w, h, "treasurechest.png")
        self.image(self.pic)
        self.nextlevelflag = False

    def collis(self, pl, X, X0):
        '''exit collision detection, assuming the parent to
        this object will always be a game class'''
        self.nextlevelflag = True 
    def getselfflag(self):
        '''return flag status for handling
        NOTE: method for setting nextlevelflag is not present. In theory,
        when nextlevelflag is TRUE, all objects will be deleted and replaced.'''
        return self.nextlevelflag


