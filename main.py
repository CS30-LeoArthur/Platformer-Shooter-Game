import pygame


# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (220, 230, 20)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTBLUE = (102, 255, 255)
SCREENWIDTH = 800
SCREENHEIGHT = 800

def rectCollide(rect1, rect2):
    return rect1.x < rect2.x + rect2.width and rect1.y < rect2.y + rect2.height and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

def checkCollision(object1, object2):
    for i in range(len(object1)):
        if rectCollide(object1[i], object2):
            return i
    return -1

class Player():
    def __init__(self, x, y, width, height, xChange, yChange, view, jumpCount):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.view = view
        self.jumpCount = jumpCount

    def jump(self):
        if self.jumpCount > 0:
            self.yChange = -7
            self.jumpCount = 0

    def goLeft(self):
        self.xChange = -3
    
    def goRight(self):
        self.xChange = 3

    def hzStop(self):
        self.xChange = 0

    def vtDefault(self):
        self.yChange = 0.1
    
    def checkVerticalPlatformCollision(self, platforms):
        PlatformIndex = checkCollision(platforms, self)
        if PlatformIndex != -1:
            self.jumpCount += 1
            if self.yChange > 0:
                self.vtDefault()
                self.y = platforms[PlatformIndex].y - self.height
            elif self.yChange < 0:
                self.vtDefault()
                self.y = platforms[PlatformIndex].y + platforms[PlatformIndex].height
            
    
    def checkHorizontalPlatformCollision(self, platforms):
        PlatformIndex = checkCollision(platforms, self)
        if PlatformIndex != -1:
            if self.xChange > 0:
                self.x = platforms[PlatformIndex].x - self.width
            elif self.xChange < 0:
                self.x = platforms[PlatformIndex].x + platforms[PlatformIndex].width
    
    def checkPlayerEdgeCollision(self, level):
        if self.x < 0:
            self.x = 0
        elif self.x > level.levelWidth - self.width:
            self.x = level.levelWidth - self.width

    def viewHorizontalEdge(self, level):
        if self.view[0] < 0:
            self.view[0] = 0
        elif self.view[0] > level.levelWidth - SCREENWIDTH:
            self.view[0] = level.levelWidth - SCREENWIDTH
    
    def viewVerticalEdge(self, level):
        if self.view[1] > 0:
            self.view[1] = 0

    def update(self, platforms, level):
        self.yChange = min(5, self.yChange + 0.2)
        self.x += self.xChange
        self.checkHorizontalPlatformCollision(platforms)
        self.y += self.yChange
        self.checkVerticalPlatformCollision(platforms)

        viewX = self.x - SCREENWIDTH / 2
        viewY = self.y - SCREENHEIGHT / 2
        self.view = [viewX, viewY]
        
        self.checkPlayerEdgeCollision(level)
        self.viewHorizontalEdge(level)
        self.viewVerticalEdge(level)

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def drawPlatform(self, screen, player):
        pygame.draw.rect(screen, GREY, [self.x - player.view[0] , self.y - player.view[1], self.width, self.height])

class LevelOne():
    def __init__(self, player, platforms, levelY, levelWidth, complete):
        self.player = player
        self.platforms = platforms
        self.levelY = levelY
        self.levelWidth = levelWidth
        self.complete = complete
        
    # A method i can use to append new platforms quickly
    def appendNewPlatform(self, x, y, width, height):
        self.platforms.append(Platform(x, y, width, height))
    
    def levelOnePlatforms(self):
        # Ground I think I will need a seperate class for the ground later because I want the player to drop through the platforms but not the ground
        self.appendNewPlatform(0, self.levelY, self.levelWidth, 50)
        self.appendNewPlatform(700, self.levelY - 750, self.levelWidth - 700, 800)
        self.appendNewPlatform(0, self.levelY - 1500, 800, 600)
        self.appendNewPlatform(0, self.levelY - 400, 500, 50)
        self.appendNewPlatform(0, self.levelY - 700, 300, 50)
        self.appendNewPlatform(800, self.levelY - 950, 600, 50)
        self.appendNewPlatform(900, self.levelY - 1150, 650, 50)
        
        # Platforms
        self.appendNewPlatform(200, self.levelY - 100, 150, 20)
        self.appendNewPlatform(200, self.levelY - 100, 150, 20)
        self.appendNewPlatform(400, self.levelY - 200, 150, 20)
        self.appendNewPlatform(600, self.levelY - 300, 100, 20)
        self.appendNewPlatform(450, self.levelY - 700, 50, 200)
        self.appendNewPlatform(100, self.levelY - 500, 100, 20)
        self.appendNewPlatform(350, self.levelY - 600, 150, 20)
        self.appendNewPlatform(1400, self.levelY - 850, 100, 20)
        
        
        # Border Walls
        self.appendNewPlatform(0, self.levelY - 1600, 50, 1600)
        self.appendNewPlatform(self.levelWidth - 50, self.levelY - 1600, 50, 1600)
        
        
    # Update method
    def updateLevel(self):
        self.player.update(self.platforms, self)
        
        
    # Drawing Methods
    
    # def drawHouse(self, screen):
    #     offsetX = self.player.view[0]
    #     offsetY = self.player.view[1]
    #     pygame.draw.rect(screen, BLUE, [500 - offsetX, 400 - offsetY, 300, self.levelY - 400], 10)
    #     pygame.draw.polygon(screen, GREY, ([500 - offsetX, 400 - offsetY], [650 - offsetX, 300 - offsetY], [800 - offsetX, 400 - offsetY]))
    
    def drawPlayer(self, screen):
        offsetX = self.player.view[0]
        offsetY = self.player.view[1]

        pygame.draw.rect(screen, RED, [self.player.x - offsetX, self.player.y - offsetY, self.player.width, self.player.height])
        
        pygame.draw.rect(screen, YELLOW, [self.player.x + self.player.width - offsetX, self.player.y - offsetY + self.player.height / 2.75, 10, 5])
        
        pygame.draw.rect(screen, YELLOW, [self.player.x + self.player.width + 10 - offsetX, self.player.y - offsetY, 5, 25])
        
        pygame.draw.rect(screen, LIGHTBLUE, [self.player.x + self.player.width + 15 - offsetX, self.player.y - offsetY + self.player.height / 3.25, 30, 10])
    
    def drawLevelOne(self, screen):
        self.drawPlayer(screen)
        
        for i in range(len(self.platforms)):
            self.platforms[i].drawPlatform(screen, self.player)




def main():
    pygame.init()
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    
    player = Player(100, 720, 30, 30, 0, 0, 0, 0)

    levelOne = LevelOne(player, [], 750, 1600, False)

    levelOne.levelOnePlatforms()
    
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    levelOne.player.goLeft()
                elif event.key == pygame.K_d:
                    levelOne.player.goRight()
                elif event.key == pygame.K_SPACE:
                    levelOne.player.jump()    
            # Stop player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.xChange < 0 or event.key == pygame.K_d and player.xChange > 0:
                    levelOne.player.hzStop()
        
        levelOne.updateLevel()
        # Drawing
        screen.fill(WHITE)

        levelOne.drawLevelOne(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
