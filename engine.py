import pygame, math, os, time
from pygame.locals import *
#Vars
metaKeySeparator = "|"
deltaTime = 1
lastTime = time.time()
physicsObjects = []

#Shizbiz

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class PhysicsObject:
    def __init__(self,posRef,xSize,ySize):
        self.position = posRef
        self._xSize = xSize
        self._ySize = ySize
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
        self.collisionData['meta'] = {}
        self.collisionData['left'] = False
        self.collisionData['right'] = False
        #X
        if(self.velocity.x != 0):
            self.position.x += self.velocity.x * deltaTime
            rect = self.Rect()
            collisions = CheckCollision(self,physicsObjects)
            for other in collisions:
                if self.velocity.x > 0:
                    rect.right = other.rect.left
                    self.collisionData['right'] = True
                    self.velocity.x = 0
                elif self.velocity.x < 0:
                    rect.left = other.rect.right
                    self.collisionData['left'] = True
                    self.velocity.x = 0
                self.position.x = rect.x
        #Y
        if(self.velocity.y != 0):
            self.position.y += self.velocity.y * deltaTime
            rect = self.Rect()
            collisions = CheckCollision(self, physicsObjects)

            if(self.velocity.y < 0):
                self.collisionData['bottom'] = False
            else:
                self.collisionData['top'] = False

            for other in collisions:
                if self.velocity.y > 0:
                    rect.bottom = other.rect.top
                    self.collisionData['bottom'] = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:
                    rect.top = other.rect.bottom
                    self.collisionData['top'] = True
                    self.velocity.y = 0
                self.position.y = rect.y
        return self.collisionData
    def AddForce(self,x,y):
        self.velocity.x += x
        self.velocity.y += y
    def ResetForce(self):
        self.velocity = Vector(0,0)

class Entity:
    def __init__(self,x,y,xSize,ySize,setupPhysics=True):
        self.name = "Unnamed Entity"
        self.position = Vector(x,y)
        self.xSize = xSize
        self.ySize = ySize
        self.rotation = 0
        self.sprite = None
        self.meta = {}
        self.physics : PhysicsObject = None
        if(setupPhysics):
            self.SetupPhysics()
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
        return Vector(self.x + int(self.xSize/2),self.y + int(self.ySize/2))
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
        surface.blit(self.sprite,(self.position.x,self.position.y))
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