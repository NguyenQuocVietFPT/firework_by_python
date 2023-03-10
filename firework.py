import pygame, sys, random, math
from pygame.locals import *

WINHEIGHT = 600
WINWIDTH = 600
FPS = 60
SIZE = 4.5
SPEED_CHANGE_SIZE = 0.05
CHANGE_SPEED = 0.07
RAD = math.pi/180
A_FALL = 1.5
NUM_BULLET = 50
SPEED_MIN = 2
SPEED_MAX = 4
TIMEW_CREATE_FW = 40
NUM_FIREWORK_MAX = 3
NUM_FIREWORK_MIN = 1
SPEED_FLY_UP_MAX = 12
SPEED_FLY_UP_MIN = 8

class Dot():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def update(self):
        if self.size > 0 :
            self.size -= SPEED_CHANGE_SIZE * 5
        else :
            self.size = 0   

    def draw(self):
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF,self.color,
            (int(self.x), int(self.y)),int(self.size))

class ButterFlyUp():
    def __init__(self, speed, x):
        self.speed = speed
        self.x = x
        self.y = WINHEIGHT
        self.dots = []
        self.size = SIZE / 2
        self.color = (255,255,100)

    def update(self):
        self.dots.append(Dot(self.x, self.y, self.size, self.color))
        self.y -= self.speed
        self.speed -= A_FALL * 0.1
        for i in range(len(self.dots)):
            self.dots[i].update()      
        i = 0
        while i < len(self.dots):
            if self.dots[i].size <= 0:
                self.dots.pop(i)
            else:
                i+=1

    def draw(self):
        pygame.draw.circle(DISPLAYSURF,self.color,
                            (int(self.x), int(self.y)),int(self.size))
        for i in range (len(self.dots)):
            self.dots[i].draw()            

class Bullet():
    def __init__(self, x, y, speed, angle, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = SIZE
        self.angle = angle
        self.color = color
    
    def update(self):
        speedX = self.speed * math.cos(self.angle * RAD)
        speedY = self.speed * -math.sin(self.angle * RAD)            

        self.x += speedX
        self.y += speedY
        self.y += A_FALL

        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0
                    
        if self.speed > 0:
            self.speed -= CHANGE_SPEED
        else:
            self.speed = 0
        
    def draw(self):
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF,self.color,
                            (int(self.x), int(self.y)),int(self.size))

class Random():
    def __init__(self):
        pass

    def color():
        colorOne = random.randint(0,255)
        colorTwo = random.randint(0,255)

        if colorOne + colorTwo >= 255:
            colorThree = random.randint(0,255)
        else:
            colorThree = random.randint(255 - colorOne - colorTwo, 255)
        
        colorList = [colorOne, colorTwo, colorThree]
        random.shuffle(colorList)
        return colorList

    def num_firework():
        return random.randint(NUM_FIREWORK_MIN, NUM_FIREWORK_MAX)

    def randomBulletFlyUp_speed():
        speed = random.uniform(SPEED_FLY_UP_MIN,SPEED_FLY_UP_MAX)
        return speed

    def randomBulletFlyUp_x():
        x = random.randint(int(WINWIDTH * 0.2), int(WINHEIGHT * 0.8))
        return x

class FireWork():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dots = []
    
        def createBullets():
            bullets = []
            color = Random.color()
            for i in range(NUM_BULLET):
                angle = (360/NUM_BULLET)*i
                speed = random.uniform(SPEED_MIN, SPEED_MAX)
                bullets.append(Bullet(self.x, self.y, speed, angle, color))

            return bullets
        self.bullets = createBullets()

    def update(self):
        for i in range(len(self.bullets)):
            self.bullets[i].update()
            self.dots.append(Dot(self.bullets[i].x, self.bullets[i].y, 
                                    self.bullets[i].size, self.bullets[i].color))

        for i in range(len(self.dots)):
            self.dots[i].update()

        i = 0
        while i < len(self.dots):
            if self.dots[i].size <= 0:
                self.dots.pop(i)
            else:
                i+=1                       

    def draw(self):
        for i in range(len(self.bullets)):
            self.bullets[i].draw()
        for i in range(len(self.dots)):
            self.dots[i].draw()                

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    fireWorks = []
    time = TIMEW_CREATE_FW
    bulletFlyUps = []

    while True:
        DISPLAYSURF.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if time == TIMEW_CREATE_FW:
                for i in range(Random.num_firework()):
                    bulletFlyUps.append(ButterFlyUp(Random.randomBulletFlyUp_speed(),
                                        Random.randomBulletFlyUp_x()))

            for i in range(len(bulletFlyUps)):
                bulletFlyUps[i].draw()
                bulletFlyUps[i].update()

            for i in range(len(fireWorks)):
                fireWorks[i].draw()
                fireWorks[i].update()           

            i = 0
            while i < len(bulletFlyUps):
                if bulletFlyUps[i].speed <= 0:
                    fireWorks.append(FireWork(bulletFlyUps[i].x, bulletFlyUps[i].y))
                    bulletFlyUps.pop(i)
                else:
                    i += 1                                             
                
            i = 0
            while i < len(fireWorks):
                if fireWorks[i].bullets[0].size <= 0:
                    fireWorks.pop(i)
                else:
                    i += 1
                    
            if time <= TIMEW_CREATE_FW:
                time += 1
            else:
                time = 0
            pygame.display.update()
            FPSCLOCK.tick(FPS)                    


if __name__ == '__main__':
    main()
