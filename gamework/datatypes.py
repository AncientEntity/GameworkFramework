class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def Translate(self,x,y):
        self.x += x
        self.y += y
    def SetPosition(self,x,y):
        self.x = x
        self.y = y
