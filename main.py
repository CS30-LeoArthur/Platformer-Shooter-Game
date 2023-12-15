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

    def update(self, platforms):
        self.yChange = min(5, self.yChange + 0.2)
        self.x += self.xChange
        self.checkHorizontalPlatformCollision(platforms)
        self.y += self.yChange
        self.checkVerticalPlatformCollision(platforms)

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def drawPlatform(self, screen):
        pygame.draw.rect(screen, GREY, [self.x, self.y, self.width, self.height])

class LevelOne():
    def __init__(self, player, platforms, groundY, groundWidth, complete):
        self.player = player
        self.platforms = platforms
        self.groundY = groundY
        self.groundWidth = groundWidth
        self.complete = complete
        
    def levelOnePlatforms(self):
        self.platforms.append(Platform(0, self.groundY, self.groundWidth, 50))
        self.platforms.append(Platform(200, self.groundY - 100, 150, 20))
        self.platforms.append(Platform(250, self.groundY - 200, 150, 20))
        self.platforms.append(Platform(300, self.groundY - 300, 150, 20))
        self.platforms.append(Platform(350, self.groundY - 400, 150, 20))
    
    def updatePlayer(self):
        self.player.update(self.platforms)
        
        
    
    def drawHouse(self, screen):
        pygame.draw.rect(screen, BLUE, [500, 400, 300, self.groundY - 400], 10)
        pygame.draw.polygon(screen, GREY, ([500, 400], [650, 300], [800, 400]), 10)
    
    def drawPlayer(self, screen):
        pygame.draw.rect(screen, RED, [self.player.x, self.player.y, self.player.width, self.player.height])
        pygame.draw.rect(screen, YELLOW, [self.player.x + self.player.width, self.player.y + self.player.height / 2.75, 10, 5])
        pygame.draw.rect(screen, YELLOW, [self.player.x + self.player.width + 10, self.player.y, 5, 25])
        pygame.draw.rect(screen, LIGHTBLUE, [self.player.x + self.player.width + 15, self.player.y + self.player.height / 3.25, 30, 10])
    
    def drawLevelOne(self, screen):
        self.drawPlayer(screen)
        self.drawHouse(screen)
        
        for i in range(len(self.platforms)):
            self.platforms[i].drawPlatform(screen)




def main():
    pygame.init()
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    
    player = Player(50, 720, 30, 30, 0, 0, 0, 0)

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
                elif event.key == pygame.K_w:
                    levelOne.player.jump()    
            # Stop player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.xChange < 0 or event.key == pygame.K_d and player.xChange > 0:
                    levelOne.player.hzStop()
        
        levelOne.updatePlayer()
        # Drawing
        screen.fill(WHITE)

        levelOne.drawLevelOne(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
