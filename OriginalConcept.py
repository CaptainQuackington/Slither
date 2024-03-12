import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Slither Game')
clock = pygame.time.Clock()

doExit = False

scrollX = 0
scrollY = 0

pelletCount = 0
class Pellet:
    def __init__(self, xpos, ypos, red, green, blue, radius):
        self.xpos = xpos
        self.ypos = ypos
        self.red = red
        self.green = green
        self.blue = blue
        self.radius = radius
        
    def draw(self, scrollX, scrollY):
        pygame.draw.circle(screen, (self.red, self.green, self.blue), ((self.xpos - scrollX), (self.ypos - scrollY)), self.radius)

class TailSegment:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), ((self.xpos- scrollX), (self.ypos - scrollY)), 12)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

xpos = 2500
ypos = 2500
Vx = 1
Vy = 1

mousepos = (0, 0)

listOfPellets = []
tail = []

randomPelletAmount = random.randrange(5000, 10000)

for i in range(randomPelletAmount):
    listOfPellets.append(Pellet(random.randrange(0, 5000),random.randrange(0, 5000),random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255),random.randrange(2, 10)))

score = 0


while not doExit:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True
        elif event.type == pygame.MOUSEMOTION:
            mousepos = event.pos
            
            Vx = (mousepos[0] / 400) - 1.5
            Vy = (mousepos[1] / 400) - 1
            
    xpos += Vx * 2.5
    ypos += Vy * 2.5
    
    # Collision detection with pellets
    i = 0
    while i < len(listOfPellets):
        p = listOfPellets[i]
        if distance(xpos, ypos, p.xpos, p.ypos) < 12 + p.radius: # Player collides with a pellet
            score += 1
            listOfPellets.pop(i)
        else:
            i += 1
    
    # Death condition
    if xpos <= 0 or xpos >= 5000 or ypos <= 0 or ypos >= 5000: # Player hits the edge
        doExit = True
    
    # Adding tail segment
    tail.insert(0, TailSegment(xpos, ypos ))
    
    # Limit tail length
    if len(tail) > 50 + score:
        tail.pop()
    
    # Scrolling
    scrollX = max(0, min(xpos - screen.get_width() / 2, 5000 - screen.get_width()))
    scrollY = max(0, min(ypos - screen.get_height() / 2, 5000 - screen.get_height()))
    
    screen.fill((255, 255, 255))
    
    # Drawing pellets
    for p in listOfPellets:
        p.draw(scrollX, scrollY)
        
    # Drawing player
    pygame.draw.circle(screen, (0, 255, 200), ((xpos - scrollX), (ypos - scrollY)), 12)
    
    # Drawing tail
    for segment in tail:
        segment.draw()
    pygame.display.flip()

pygame.quit()
