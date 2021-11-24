import pygame, math, os, time
from .datatypes import *
#Vars
metaKeySeparator = "|"
deltaTime = 1
lastTime = time.time()
physicsObjects = []
camera = Vector(0,0)

#Shizbiz

class PhysicsObject:
    def __init__(self,posRef,xSize,ySize):
        self.position = posRef
        self._xSize = xSize
        self._ySize = ySize
        self._name = "Unnamed Object"
        self._tag = "Untagged"
        self.velocity = Vector(0,0)
        self.rect = pygame.Rect(posRef.x,posRef.y,xSize,ySize)
        self.collisionData = {'top':False,'bottom':False,'left':False,'right':False,'meta':{}}
        physicsObjects.append(self)
    def GetSize(self):
        return Vector(self._xSize,self._ySize)
    def Rect(self) -> pygame.Rect:
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        return self.rect
    def CheckCollision(self,other):
        if(other == self):
            return False
        return self.Rect().colliderect(other.rect)
    def Update(self):
        #collisionData = {'top':False,'bottom':False,'left':False,'right':False,'meta':{}}
        self.RawMove(self.velocity)
        return self.collisionData
    def RawMove(self,displacement):
        self.collisionData['meta'] = {}
        self.collisionData['left'] = False
        self.collisionData['right'] = False
        # X
        if (displacement.x != 0):
            self.position.x += displacement.x * deltaTime
            rect = self.Rect()
            collisions = CheckCollision(self, physicsObjects)
            for other in collisions:
                if displacement.x > 0:
                    rect.right = other.rect.left
                    self.collisionData['right'] = True
                    self.velocity.x = 0
                elif displacement.x < 0:
                    rect.left = other.rect.right
                    self.collisionData['left'] = True
                    self.velocity.x = 0
                self.position.x = rect.x
        # Y
        if (displacement.y != 0):
            self.position.y += displacement.y * deltaTime
            rect = self.Rect()
            collisions = CheckCollision(self, physicsObjects)

            if (displacement.y < 0):
                self.collisionData['bottom'] = False
            else:
                self.collisionData['top'] = False

            for other in collisions:
                if displacement.y > 0:
                    rect.bottom = other.rect.top
                    self.collisionData['bottom'] = True
                    self.velocity.y = 0
                elif displacement.y < 0:
                    rect.top = other.rect.bottom
                    self.collisionData['top'] = True
                    self.velocity.y = 0
                self.position.y = rect.y
    def AddForce(self,x,y):
        self.velocity.x += x
        self.velocity.y += y
    def ResetForce(self):
        self.velocity = Vector(0,0)

class Entity:
    def __init__(self,x,y,xSize,ySize,setupPhysics=True):
        self.name = "Unnamed Object"
        self.tag = "Untagged"
        self.position = Vector(x,y)
        self.xSize = xSize
        self.ySize = ySize
        self.rotation = 0
        self.sprite = None
        self.meta = {}
        self.physics : PhysicsObject = None
        if(setupPhysics):
            self.SetupPhysics()
    def SetName(self,newName):
        self.name = newName
        self.physics._name = newName
    def SetTag(self,newTag):
        self.tag = newTag
        self.physics._tag = newTag
    def Translate(self,x,y):
        self.position.x += x
        self.position.y += y
    def SetPosition(self,x,y):
        self.position.x = x
        self.position.y = y
    def Rect(self):
        return pygame.Rect(self.x,self.y,self.xSize,self.ySize)
    def StretchToSprite(self):
        self.xSize = self.sprite.get_width()
        self.ySize = self.sprite.get_height()
        self.physics.rect.width = self.xSize
        self.physics.rect.height = self.ySize
    def Center(self):
        return Vector(self.position.x + (self.xSize/2.0),self.position.y + (self.ySize/2.0))
    def SetMeta(self,key,value):
        keys = key.split(metaKeySeparator) #Find subkeys
        lastDict = self.meta
        length = len(keys)
        c = 0
        for key in keys[:length-1]:
            if(key not in lastDict):
                lastDict[key] = {}
                lastDict = lastDict[key]
            else:
                lastDict = lastDict[key]
                if (isinstance(lastDict,dict) == False):
                    raise Exception("Invalid Subkey leads to something that isn't a dictionary: ",keys)
        lastDict[keys[length-1]] = value
    def GetMeta(self,key):
        keys = key.split(metaKeySeparator)
        lastDict = self.meta
        length = len(keys)
        c = 0
        for key in keys[:length-1]:
            if(key not in lastDict):
                raise Exception("Key path doesn't exist", keys)
            else:
                lastDict = lastDict[key]
                if (isinstance(lastDict,dict) == False):
                    raise Exception("Key path doesn't exist",keys)
        return lastDict[keys[length-1]]
    def SetupPhysics(self):
        self.physics = PhysicsObject(self.position,self.xSize,self.ySize)
    def Draw(self,surface : pygame.Surface):
        renderPos = Vector(self.position.x-int(camera.x),self.position.y-int(camera.y))
        if(renderPos.x < -self.sprite.get_width() or renderPos.x > surface.get_width()+self.sprite.get_width()):
            return
        if(renderPos.y < -self.sprite.get_height() or renderPos.y > surface.get_height()+self.sprite.get_height()):
            return
        surface.blit(self.sprite,(renderPos.x,renderPos.y))
    def GetCollisionData(self):
        return self.physics.collisionData


#Helper Methods
def CheckCollision(me,others : list):
    collidingWith = []
    physMe = me
    if(isinstance(me,PhysicsObject) == False):
        physMe = me.physics
    for obj in others:
        physOther = obj
        if(isinstance(obj,PhysicsObject) == False):
            physOther = obj.physics
        if(physMe.CheckCollision(physOther)):
            collidingWith.append(physOther)
    return collidingWith

def StartDeltaTime(): # Use Once
    global deltaTime,lastTime
    deltaTime = 0
    lastTime = time.time()
def CalculateDeltaTime(): # Use Every Frame, things like physics rely on this.
    global deltaTime,lastTime
    deltaTime = time.time() - lastTime
    lastTime = time.time()
