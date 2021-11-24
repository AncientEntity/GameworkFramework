import pygame
from engine import *

pygame.init()
screen = pygame.display.set_mode((800,600))
display = pygame.Surface((400,300))
entities = []

for y in range(10):
    for x in range(14):
        if(y == 8 or (y == 7 and x > 6)):
            Ent = Entity(x * 16, y * 16, 16, 16)
            Ent.sprite = pygame.image.load("ground.png")
            entities.append(Ent)

Ent = Entity(100,50,16,16)
Ent.sprite = pygame.image.load("ground.png")
entities.append(Ent)

player = Entity(50,20,0,0)
player.sprite = pygame.image.load("player.png")
player.StretchToSprite()
entities.append(player)
StartDeltaTime()
while True:
    display.fill((255,255,255))
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE and player.GetCollisionData()['bottom']):
                player.physics.velocity.y = -150
    if(pressed[pygame.K_a]):
        player.physics.velocity.x = -25
    elif(pressed[pygame.K_d]):
        player.physics.velocity.x = 25
    else:
        player.physics.velocity.x = 0

    player.physics.velocity.y += 2
    for obj in entities:
        obj : Entity
        obj.physics.Update()
        obj.Draw(display)
    tempDisplay = pygame.transform.scale(display,(800*2,600*2))
    screen.blit(tempDisplay,(0,0))
    pygame.display.update()
    CalculateDeltaTime()