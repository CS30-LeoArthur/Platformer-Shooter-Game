import pygame

# To Do List
# - Work on levels
# - Player Movement Options
# - Create a weapon for the player
# - Power ups
# - Create Enemy Class
# - Create Platform Class
# - Player Health Bar

# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (220, 230, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHTBLUE = (102, 255, 255)
SCREENWIDTH = 800
SCREENHEIGHT = 800

# Helper Functions
def rectCollide(rect1, rect2):
    return rect1.x < rect2.x + rect2.width and rect1.y < rect2.y + rect2.height and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

def checkCollision(object1, object2):
    for i in range(len(object1)):
        if rectCollide(object1[i], object2):
            return i
    return -1

def mouse_position():
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    return mouse_x, mouse_y

def distance_calc(player):
    run = mouse_position()[0] - player.x
    rise = mouse_position()[1] - player.y
    distance = math.sqrt(run**2 + rise**2)
    dx = player.x + (run * player.radius / distance)
    dy = player.y + (rise * player.radius / distance)
    return dx, dy

# To do
# - Create Enemy Class
class Enemy():
    def __init__(self, x, y, width, height, xChange, yChange, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.health = health
    
    def goLeft(self):
        self.xChange = -3
        
    def goRight(self):
        self.xChange = 3
    
    def drawEnemy(self, screen, player):
        pygame.draw.rect(screen, RED, [self.x - player.view[0], self.y - player.view[1], self.width, self.height])


class Player():
    def __init__(self, x, y, width, height, xChange, yChange, view, jumpCount, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.view = view
        self.jumpCount = jumpCount
        self.health = health

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
    
    def checkEnemyCollision(self, enemies):
        enemyIndex = checkCollision(enemies, self)
        if enemyIndex != -1:
            self.health -= 20
            if self.xChange > 0:
                self.x -= 20
            elif self.xChange < 0:
                self.x += 20
    
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
        if self.view[1] < level.levelHeight:
            self.view[1] = level.levelHeight

    def update(self, platforms, enemy, level):
        self.yChange = min(5, self.yChange + 0.2)
        self.x += self.xChange
        self.checkHorizontalPlatformCollision(platforms)
        self.checkEnemyCollision(enemy)
        self.y += self.yChange
        self.checkVerticalPlatformCollision(platforms)

        viewX = self.x - SCREENWIDTH / 2
        viewY = self.y - SCREENHEIGHT / 2
        self.view = [viewX, viewY]
        
        self.checkPlayerEdgeCollision(level)
        self.viewHorizontalEdge(level)
        self.viewVerticalEdge(level)
    
    def drawHealthBar(self, screen):
        healthBarWidth = 200
        healthBar = self.health * 2
        pygame.draw.rect(screen, RED, [0, SCREENHEIGHT - 50, healthBarWidth, 50])
        pygame.draw.rect(screen, GREEN, [0, SCREENHEIGHT - 50, healthBar, 50])
        pygame.draw.rect(screen, BLACK, [0, SCREENHEIGHT - 52, healthBarWidth, 52], 2)

    def resetPlayerLevelOne(self):
        self.x = 100
        self.y = 720
        self.health = 100

    def drawPlayer(self, screen):
        offsetX = self.view[0]
        offsetY = self.view[1]

        pygame.draw.rect(screen, BLUE, [self.x - offsetX, self.y - offsetY, self.width, self.height])
        
        pygame.draw.rect(screen, YELLOW, [self.x + self.width - offsetX, self.y - offsetY + self.height / 2.75, 10, 5])
        
        pygame.draw.rect(screen, YELLOW, [self.x + self.width + 10 - offsetX, self.y - offsetY, 5, 25])
        
        pygame.draw.rect(screen, LIGHTBLUE, [self.x + self.width + 15 - offsetX, self.y - offsetY + self.height / 3.25, 30, 10])

        self.drawHealthBar(screen)

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def drawPlatform(self, screen, player):
        pygame.draw.rect(screen, GREY, [self.x - player.view[0] , self.y - player.view[1], self.width, self.height])

class Level():
    def __init__(self, player, platforms, enemies, groundY, levelHeight, levelWidth, levelNumber):
        self.player = player
        self.platforms = platforms
        self.enemies = enemies
        self.groundY = groundY
        self.levelHeight = levelHeight
        self.levelWidth = levelWidth
        self.levelNumber = levelNumber
        
    # A method i can use to append new platforms quickly
    def appendNewPlatform(self, x, y, width, height):
        self.platforms.append(Platform(x, y, width, height))
    
    # Platforms
    def levelOnePlatforms(self):
        # Ground I think I will need a seperate class for the ground later because I want the player to drop through the platforms but not the ground
        self.appendNewPlatform(0, self.groundY, self.levelWidth, 50)
        self.appendNewPlatform(700, self.groundY - 750, self.levelWidth - 700, 800)
        self.appendNewPlatform(0, self.groundY - 1350, 800, 450)
        self.appendNewPlatform(0, self.groundY - 400, 500, 50)
        self.appendNewPlatform(0, self.groundY - 700, 300, 50)
        self.appendNewPlatform(800, self.groundY - 950, 600, 50)
        self.appendNewPlatform(900, self.groundY - 1150, 650, 50)
        self.appendNewPlatform(800, self.groundY - 1350, 600, 50)
        
        # Platforms
        self.appendNewPlatform(200, self.groundY - 100, 150, 20)
        self.appendNewPlatform(200, self.groundY - 100, 150, 20)
        self.appendNewPlatform(400, self.groundY - 200, 150, 20)
        self.appendNewPlatform(600, self.groundY - 300, 100, 20)
        self.appendNewPlatform(450, self.groundY - 700, 50, 200)
        self.appendNewPlatform(100, self.groundY - 500, 100, 20)
        self.appendNewPlatform(350, self.groundY - 600, 150, 20)
        self.appendNewPlatform(1450, self.groundY - 850, 100, 20)
        self.appendNewPlatform(800, self.groundY - 1050, 100, 20)
        self.appendNewPlatform(1450, self.groundY - 1250, 100, 20)
        
        
        # Border Walls
        self.appendNewPlatform(0, self.levelHeight, 50, 1600)
        self.appendNewPlatform(self.levelWidth - 50, self.levelHeight, 50, 1600)
        self.appendNewPlatform(0, self.levelHeight, self.levelWidth, 50)

    def levelTwoPlatforms(self):
        self.appendNewPlatform(0, self.groundY, self.levelWidth, 50)

    # Enemies
    def levelOneEnemies(self):
        self.enemies.append(Enemy(100, self.groundY - 700 - 20, 20, 20, 0, 0, 15))
        self.enemies.append(Enemy(200, self.groundY - 20, 20, 20, 0, 0, 15))
    
    def restartLevel(self):
        if self.levelNumber == "one":
            if self.platforms != [] and self.enemies != []:
                self.platforms.clear()
                self.enemies.clear()
                self.levelOnePlatforms()
                self.levelOneEnemies()
                self.player.resetPlayerLevelOne()
        elif self.levelNumber == "two":
            if self.platforms != [] and self.enemies != []:
                self.platforms.clear()
                self.enemies.clear()
                self.levelTwoPlatforms()
        
        
    # Update method
    def updateLevel(self):
        if self.levelNumber == "one":
            if self.platforms == []:
                self.levelOnePlatforms()
                self.levelOneEnemies()
        
        if self.levelNumber == "two":
            if self.platforms == []:
                self.levelTwoPlatforms()

        if self.player.health <= 0:
            self.restartLevel()
            
        self.player.update(self.platforms, self.enemies, self)
        
        
    # Drawing Methods
    
    # def drawHouse(self, screen):
    #     offsetX = self.player.view[0]
    #     offsetY = self.player.view[1]
    #     pygame.draw.rect(screen, BLUE, [500 - offsetX, 400 - offsetY, 300, self.groundY - 400], 10)
    #     pygame.draw.polygon(screen, GREY, ([500 - offsetX, 400 - offsetY], [650 - offsetX, 300 - offsetY], [800 - offsetX, 400 - offsetY]))
    
    def drawExit(self, screen):
        offsetX = self.player.view[0]
        offsetY = self.player.view[1]

        pygame.draw.rect(screen, BLUE, [150 - offsetX, self.groundY - 1500 - offsetY, 100, 150])
    
    def drawLevel(self, screen):
        self.drawExit(screen)
        
        for i in range(len(self.platforms)):
            self.platforms[i].drawPlatform(screen, self.player)
        
        for i in range(len(self.enemies)):
            self.enemies[i].drawEnemy(screen, self.player)

        self.player.drawPlayer(screen)



def main():
    pygame.init()
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    
    player = Player(100, 720, 30, 30, 0, 0, 0, 0, 100)

    level = Level(player, [], [], 750, -850, 1600, "one")
    
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    level.player.goLeft()
                elif event.key == pygame.K_d:
                    level.player.goRight()
                elif event.key == pygame.K_SPACE:
                    level.player.jump()    
            # Stop player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.xChange < 0 or event.key == pygame.K_d and player.xChange > 0:
                    level.player.hzStop()
    
        # Logic
        level.updateLevel()
        
        # Drawing
        screen.fill(WHITE)

        level.drawLevel(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
