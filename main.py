import pygame

# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
SCREENWIDTH = 800
SCREENHEIGHT = 800

class Player():
    def __init__(self, x, y, width, height, xChange, yChange, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xChange = xChange
        self.yChange = yChange
        self.health = health
    
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




def main():
    pygame.init()
    
    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    
    # Loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Logic
        
        # Drawing
        screen.fill(WHITE)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
