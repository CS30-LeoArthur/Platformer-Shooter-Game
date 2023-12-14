import pygame

# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
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

    def go_left(self):
        self.xChange = -3
    
    def go_right(self):
        self.xChange = 3

    def hzstop(self):
        self.xChange = 0
    
    def startFall(self):
        self.change_y = -0.1

    def update(self):
        self.yChange = min(5, self.yChange + 0.2)
        self.x += self.xChange
        self.y += self.yChange

    
    def drawPlayer(self, screen):
        pygame.draw.rect(screen, RED, [self.x, self.y, self.width, self.height])

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

    def checkVerticalPlatformCollision(self):
        platformIndex = checkCollision(self.platforms, self)
        if platformIndex != -1:
            self.player.jump_count += 1
            if self.change_y > 0:
                self.player.vt_default()
                self.player.y = self.platforms[platformIndex].y - self.height
            elif self.change_y < 0:
                self.player.startFall()
                self.player.y = self.platforms[platformIndex].y + self.platforms[platformIndex].height
    
    def drawHouse(self, screen):
        pygame.draw.rect(screen, BLUE, [500, 400, 300, self.groundY - 400], 10)
        pygame.draw.polygon(screen, GREY, ([500, 400], [650, 300], [800, 400]), 10)
    
    def drawLevelOne(self, screen):
        self.player.drawPlayer(screen)
        self.drawHouse(screen)
        
        for i in range(len(self.platforms)):
            self.platforms[i].drawPlatform(screen)




def main():
    pygame.init()
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    
    player = Player(50, 730, 20, 20, 0, 0, 0, 0)

    levelOne = LevelOne(player, [], 750, 1600, False)
    
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.K_a:
                player.go_left()
            elif event.type == pygame.K_d:
                player.go_right()
            elif event.type == pygame.K_w:
                player.jump()

        # Logic
        levelOne.levelOnePlatforms()
        levelOne.checkVerticalPlatformCollision()
        player.update()
        
        # Drawing
        screen.fill(WHITE)

        levelOne.drawLevelOne(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
