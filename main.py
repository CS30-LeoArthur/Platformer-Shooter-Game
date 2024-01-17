import pygame
import math
import random

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

def belowCollide(rect1, rect2):
    return rect1.y < rect2.y + rect2.height + 1 and rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

# With one list
def checkCollision(object1, object2):
    for i in range(len(object1)):
        if rectCollide(object1[i], object2):
            return i
    return -1

def checkBelow(object1, object2):
    for i in range(len(object1)):
        if belowCollide(object1[i], object2):
            return i
    return -1

def mouse_position():
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    return mouse_x, mouse_y

def distanceCalc(player):
    run = mouse_position()[0] - (player.x + player.width / 2 - player.view[0])
    rise = mouse_position()[1] - (player.y + player.height / 2 - player.view[1])
    distance = math.sqrt(run**2 + rise**2)
    dx = player.x + player.width / 2 + (run * 20 / distance)
    dy = player.y + player.height / 2 + (rise * 20 / distance)
    return dx, dy

def distanceCalcBullets(player):
    run = mouse_position()[0] - (player.x + player.width / 2 - player.view[0])
    rise = mouse_position()[1] - (player.y + player.height / 2 - player.view[1])
    distance = math.sqrt(run**2 + rise**2)
    dx = run * 5 / distance
    dy = rise * 5 / distance
    return dx, dy

class Bullet():
    def __init__(self, x, y, width, height, xChange, yChange):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange

    def platformCollision(self, platforms, level):
        platformIndex = checkCollision(platforms, self)
        if platformIndex != -1:
            level.bullets.remove(self)
            
    
    def enemyBulletCollision(self, enemies, level):
        enemyIndex = checkCollision(enemies, self)
        if enemyIndex != -1:
            level.enemies[enemyIndex].health -= 5
            level.bullets.remove(self)

    
    def update(self):
        self.x += self.xChange
        self.y += self.yChange
    
    def checkBulletCollision(self, platforms, enemies, level):
        self.platformCollision(platforms, level)
        self.enemyBulletCollision(enemies, level)
    
    def drawBullet(self, screen, player):
        offsetX = player.view[0]
        offsetY = player.view[1]

        pygame.draw.ellipse(screen, YELLOW, [self.x - offsetX, self.y - offsetY, self.width, self.height])

# To do
# - Create Enemy Class
class Enemy():
    def __init__(self, x, y, width, height, xChange, yChange, health, walking, walkingTimer):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.health = health
        self.walking = walking
        self.walkingTimer = walkingTimer

    def goLeft(self):
        self.xChange = -3
        
    def goRight(self):
        self.xChange = 3
    
    def vtDefault(self):
        self.yChange = 0.1

    def horizontalCollision(self, platforms):
        platformIndex = checkCollision(platforms, self)
        if platformIndex != -1:
            if self.xChange > 0:
                self.x = platforms[platformIndex].x - self.width
            elif self.xChange < 0:
                self.x = platforms[platformIndex].x + platforms[platformIndex].width

    def verticalCollision(self, platforms):
        platformIndex = checkCollision(platforms, self)
        if platformIndex != -1:
            if self.yChange > 0:
                self.y = platforms[platformIndex].y - self.height
                self.vtDefault()
            elif self.yChange < 0:
                self.y= platforms[platformIndex].y + platforms[platformIndex].height
                self.vtDefault()

    def stopWalkingAtLedge(self, platforms):
        platformIndex = checkBelow(platforms, self)
        if platformIndex != -1:
            if self.x + self.width > platforms[platformIndex].x + platforms[platformIndex].width:
                self.x = platforms[platformIndex].x + platforms[platformIndex].width - self.width
            elif self.x < platforms[platformIndex].x:
                self.x = platforms[platformIndex].x

    def randomWalking(self):
        randNum = random.random()
        if self.walking == True:
            self.walkingTimer = max(0, self.walkingTimer - 1)
            if self.walkingTimer <= 0:
                self.walking == False
        elif randNum < 0.01:
            self.goLeft()
            self.walkingTimer = random.randint(30, 90)
        elif randNum > 0.99:
            self.goRight()
            self.walkingTimer = random.randint(30, 90)

    def checkEnemyHealth(self, level):
        if self.health <= 0:
            level.enemies.remove(self)
    
    def update(self, platforms, level):
        self.yChange = min(5, self.yChange + 0.2)
        
        self.randomWalking()
        
        self.x += self.xChange
        self.horizontalCollision(platforms)
        
        self.y += self.yChange
        self.verticalCollision(platforms)
        
        self.stopWalkingAtLedge(platforms)
        self.checkEnemyHealth(level)
    
    def drawHealthBar(self, screen, player):
        offsetX = player.view[0]
        offsetY = player.view[1]
        healthBarWidth = 40
        pygame.draw.rect(screen, RED, [self.x - 10 - offsetX, self.y - 50 - offsetY, healthBarWidth, 10])
        pygame.draw.rect(screen, GREEN, [self.x - 10 - offsetX, self.y - 50 - offsetY, self.health * 2, 10])
        pygame.draw.rect(screen, BLACK, [self.x - 12 - offsetX, self.y - 52 - offsetY, healthBarWidth + 2, 14], 2)
    
    def drawEnemy(self, screen, player):
        pygame.draw.rect(screen, RED, [self.x - player.view[0], self.y - player.view[1], self.width, self.height])
        self.drawHealthBar(screen, player)

class Player():

    def __init__(self, x, y, width, height, xChange, yChange, view, jumpCount, dashCooldown, dashDuration, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.view = view
        self.jumpCount = jumpCount
        self.dashCooldown = dashCooldown
        self.dashDuration = dashDuration
        self.health = health

    def jump(self):
        if self.jumpCount > 0:
            self.yChange = -7
            self.jumpCount = 0
    
    def dashTimer(self):
        if self.dashDuration > 0:
            self.dashDuration -= 1
    
    def dash(self):
        if self.xChange > 0 and self.dashCooldown > 90:
            self.xChange = 8
            self.dashDuration = 30
            self.dashCooldown = 0
        elif self.xChange < 0 and self.dashCooldown > 90:
            self.xChange = -8
            self.dashDuration = 30
            self.dashCooldown = 0
    
    def dashStop(self):
        if self.xChange > 0 and self.dashDuration == 0:
            self.xChange = 3
        elif self.xChange < 0 and self.dashDuration == 0:
            self.xChange = -3
       

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

    def resetPlayer(self, level):
        if level.levelNumber == 1:
            self.x = 100
            self.y = 770
            self.xChange = 0
            self.yChange = 0
            self.health = 100
        elif level.levelNumber == 2:
            self.x = 1500
            self.y = 770
            self.xChange = 0
            self.yChange = 0
            self.health = 100

        elif level.levelNumber == 3:
            self.x = 100
            self.y = 770
            self.xChange = 0
            self.yChange = 0
            self.health = 100

    def update(self, platforms, enemy, level):
        self.yChange = min(5, self.yChange + 0.2)
        self.x += self.xChange
        self.checkHorizontalPlatformCollision(platforms)
        self.checkEnemyCollision(enemy)
        self.y += self.yChange
        self.checkVerticalPlatformCollision(platforms)
        
        self.dashCooldown += 1
        if self.dashDuration > 0:
            self.dashDuration -= 1

        if self.dashDuration == 0:
            self.dashStop()

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

    def drawPlayer(self, screen):
        offsetX = self.view[0]
        offsetY = self.view[1]

        pygame.draw.rect(screen, BLUE, [self.x - offsetX, self.y - offsetY, self.width, self.height])
        
        pygame.draw.line(screen, GREY, [(self.x + self.width / 2) - offsetX, (self.y + self.height / 2) - offsetY], [distanceCalc(self)[0] - offsetX, distanceCalc(self)[1] - offsetY], 11)

        self.drawHealthBar(screen)

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def drawPlatform(self, screen, player):
        pygame.draw.rect(screen, GREY, [self.x - player.view[0] , self.y - player.view[1], self.width, self.height])

class Exit():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def checkExitCollide(self, player, level):
        if rectCollide(self, player):
            level.levelNumber += 1
            level.restartLevel()
            
    
    def drawExit(self, screen, player):
        pygame.draw.rect(screen, BLACK, [self.x - player.view[0] , self.y - player.view[1], self.width, self.height])

class Level():
    def __init__(self, player, platforms, enemies, exit, bullets, groundY, levelHeight, levelWidth, levelNumber):
        self.player = player
        self.platforms = platforms
        self.enemies = enemies
        self.exit = exit
        self.bullets = bullets
        self.groundY = groundY
        self.levelHeight = levelHeight
        self.levelWidth = levelWidth
        self.levelNumber = levelNumber
        
    # A method i can use to append new platforms quickly
    def appendNewPlatform(self, x, y, width, height):
        self.platforms.append(Platform(x, y, width, height))
    
    # Platforms
    def levelOnePlatforms(self):
        # Thick Platforms
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
        self.appendNewPlatform(800, self.groundY - 800, 800, 650)
        self.appendNewPlatform(500, self.groundY - 100, 100, 100)
        self.appendNewPlatform(50, self.groundY - 150, 100, 150)
        self.appendNewPlatform(50, self.groundY - 250, 50, 20)
        self.appendNewPlatform(200, self.groundY - 300, 150, 20)
        self.appendNewPlatform(450, self.groundY - 400, 150, 20)
        self.appendNewPlatform(750, self.groundY - 500, 50, 20)
        self.appendNewPlatform(50, self.levelHeight, 600, 1020)
        self.appendNewPlatform(650, self.groundY - 600, 50, 20)
        self.appendNewPlatform(750, self.groundY - 700, 50, 20)
        self.appendNewPlatform(650, self.groundY - 800, 50, 20)
        self.appendNewPlatform(1000, self.groundY - 900, 200, 20)
        self.appendNewPlatform(1000, self.groundY - 1100, 200, 20)
        self.appendNewPlatform(1000, self.groundY - 1300, 200, 20)
        self.appendNewPlatform(650, self.groundY - 1000, 200, 20)
        self.appendNewPlatform(1350, self.groundY - 1000, 200, 20)
        self.appendNewPlatform(650, self.groundY - 1200, 200, 20)
        self.appendNewPlatform(1350, self.groundY - 1200, 200, 20)
        
        self.appendNewPlatform(0, self.groundY, self.levelWidth, 50)
        self.appendNewPlatform(0, self.levelHeight, 50, 1600)
        self.appendNewPlatform(0, self.levelHeight, self.levelWidth, 50)
        self.appendNewPlatform(self.levelWidth - 50, self.levelHeight, 50, 1200)
    
    def levelThreePlatforms(self):
        self.appendNewPlatform(700, self.groundY - 1200, 200, 1200)
        self.appendNewPlatform(500, self.groundY - 100, 200, 20)
        self.appendNewPlatform(50, self.groundY - 200, 200, 20)
        self.appendNewPlatform(500, self.groundY - 300, 200, 20)
        self.appendNewPlatform(50, self.groundY - 400, 200, 20)
        self.appendNewPlatform(500, self.groundY - 500, 200, 20)
        self.appendNewPlatform(50, self.groundY - 600, 200, 20)
        self.appendNewPlatform(500, self.groundY - 700, 200, 20)
        self.appendNewPlatform(50, self.groundY - 800, 200, 20)
        self.appendNewPlatform(500, self.groundY - 900, 200, 20)
        self.appendNewPlatform(50, self.groundY - 1000, 200, 20)
        self.appendNewPlatform(500, self.groundY - 1100, 200, 20)
        self.appendNewPlatform(900, self.groundY - 1200, 550, 50)
        self.appendNewPlatform(1000, self.groundY - 1000, 550, 50)
        self.appendNewPlatform(900, self.groundY - 800, 550, 50)
        self.appendNewPlatform(1000, self.groundY - 600, 550, 50)
        self.appendNewPlatform(900, self.groundY - 400, 550, 50)
        self.appendNewPlatform(1000, self.groundY - 200, 550, 50)
        
        self.appendNewPlatform(0, self.groundY, self.levelWidth, 50)
        self.appendNewPlatform(0, self.levelHeight, 50, 1600)
        self.appendNewPlatform(0, self.levelHeight, self.levelWidth, 50)
        self.appendNewPlatform(self.levelWidth - 50, self.levelHeight, 50, 1600)

    # Enemies
    def levelOneEnemies(self):
        self.enemies.append(Enemy(100, self.groundY - 720, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(400, self.groundY - 20, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1200, self.groundY - 820, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1200, self.groundY - 1020, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1200, self.groundY - 1120, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1200, self.groundY - 1320, 20, 20, 0, 0, 20, False, 0))

    def levelTwoEnemies(self):
        self.enemies.append(Enemy(100, self.groundY - 20, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(500, self.groundY - 420, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1050, self.groundY - 1120, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1050, self.groundY - 820 , 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1050, self.groundY - 920, 20, 20, 0, 0, 20, False, 0))

    def levelThreeEnemies(self):
        self.enemies.append(Enemy(600, self.groundY - 120, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(100, self.groundY - 420, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(600, self.groundY - 720, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(100, self.groundY - 1020, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1100, self.groundY - 1020, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1100, self.groundY - 820, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1100, self.groundY - 620, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1100, self.groundY - 420, 20, 20, 0, 0, 20, False, 0))
        self.enemies.append(Enemy(1100, self.groundY - 220, 20, 20, 0, 0, 20, False, 0))

    # Exit
    def appendExits(self, exit):
        self.exit.append(exit)
        
    def levelOneExit(self):
        self.appendExits(Exit(150, self.groundY - 1500, 100, 150))
    
    def levelTwoExit(self):
        self.appendExits(Exit(1050, self.groundY - 1450, 100, 150))
    
    def levelThreeExit(self):
        self.appendExits(Exit(1300, self.groundY - 150, 100, 150))
    
    def bulletVector(self):
        bulletSpeedX = distanceCalcBullets(self.player)[0]
        bulletSpeedY = distanceCalcBullets(self.player)[1]
        return bulletSpeedX, bulletSpeedY

    def createBullet(self):
        self.bullets.append(Bullet(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 10, 10, self.bulletVector()[0], self.bulletVector()[1]))
    
    def restartLevel(self):
        if self.levelNumber == 1:
            if self.platforms != [] and self.enemies != []:
                self.platforms.clear()
                self.enemies.clear()
                self.bullets.clear()
                self.exit.clear()
                self.levelOnePlatforms()
                self.levelOneEnemies()
                self.levelOneExit()
                self.player.resetPlayer(self)
        elif self.levelNumber == 2:
            if self.platforms != [] and self.enemies != []:
                self.platforms.clear()
                self.enemies.clear()
                self.bullets.clear()
                self.exit.clear()
                self.levelTwoPlatforms()
                self.levelTwoEnemies()
                self.levelTwoExit()
                self.player.resetPlayer(self)
        elif self.levelNumber == 3:
            if self.platforms != [] and self.enemies != []:
                self.platforms.clear()
                self.enemies.clear()
                self.bullets.clear()
                self.exit.clear()
                self.levelThreePlatforms()
                self.levelThreeExit()
                self.levelThreeEnemies()
                self.player.resetPlayer(self)
        
    def endGame(self):
        if self.levelNumber == 4:
            print("YOU WIN!")
            pygame.quit()
        
        
    # Update method
    def updateLevel(self):
        if self.levelNumber == 1:
            if self.platforms == []:
                self.levelOnePlatforms()
                self.levelOneEnemies()
                self.levelOneExit()
        
        if self.levelNumber == 2:
            if self.platforms == []:
                self.levelTwoPlatforms()
                self.levelOneEnemies()
                self.levelTwoExit()
        
        if self.levelNumber == 3:
            if self.platforms == []:
                self.levelThreePlatforms()
                self.levelThreeExit()
                self.levelThreeEnemies

        if self.player.health <= 0:
            self.restartLevel()

        self.player.update(self.platforms, self.enemies, self)
        self.exit[0].checkExitCollide(self.player, self)
        
        
        
        for i, e in reversed(list(enumerate(self.enemies))):
            self.enemies[i].update(self.platforms, self)
        
        for i in range(len(self.bullets)):
            self.bullets[i].update()
        
        for i, e in reversed(list(enumerate(self.bullets))):
            self.bullets[i].checkBulletCollision(self.platforms, self.enemies, self)
        
        self.endGame()
            
    
    def drawLevel(self, screen):
        for i in range(len(self.platforms)):
            self.platforms[i].drawPlatform(screen, self.player)
        
        for i in range(len(self.enemies)):
            self.enemies[i].drawEnemy(screen, self.player)

        for i in range(len(self.bullets)):
            self.bullets[i].drawBullet(screen, self.player)

        for i in range(len(self.exit)):
            self.exit[i].drawExit(screen, self.player)

        self.player.drawPlayer(screen)



def main():
    pygame.init()

    print("Use A and D to move left and right. Use space to jump. Click in the direction you want the player to shoot. Use shift to dash for a short duration, dash has a cooldown of 1.5 seconds. Beat all three levels to win the game. Have Fun!")
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock() 
    
    player = Player(100, 770, 30, 30, 0, 0, 0, 1, 0, 0, 100)

    level = Level(player, [], [], [], [], 750, -850, 1600, 1)
    
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    level.player.goLeft()
                elif event.key == pygame.K_d:
                    level.player.goRight()
                elif event.key == pygame.K_SPACE:
                    level.player.jump()    
                elif event.key == pygame.K_LSHIFT:
                    level.player.dash()
            # Stop player
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.xChange < 0 or event.key == pygame.K_d and player.xChange > 0:
                    level.player.hzStop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                level.createBullet()
                
    
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
