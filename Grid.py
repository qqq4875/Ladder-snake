import pygame, SimpleText, sys

class Grid:
    def __init__(self, surface, grid_size=60, starting_point=(0, 0)):
        self.surface = surface
        self.grid_size = grid_size
        self.left_margin = starting_point[0]
        self.top_margin = starting_point[1]

    def drawGrid(self, width=1, grid_color=[255, 255, 255], num_color=[255, 255, 255], num_size=30):

        # Draw square grids

        # Default display width = 600
        # Default display height = 600

        # Grid's length doesn't change on display width nor height
        # Grid's default position always start at (0, 0)

        order = 1
        Grid_counter = 1

        for y in range(9, -1, -1):
            if order == 1:
                for x in range(0, 10, order):
                    Grid_num = SimpleText.SimpleText(self.surface, [x*self.grid_size + self.left_margin + width, y*self.grid_size + self.top_margin + width], str(Grid_counter), num_color, num_size)
                    rect = pygame.Rect(x*self.grid_size + self.left_margin, y*self.grid_size + self.top_margin, self.grid_size, self.grid_size)

                    pygame.draw.rect(self.surface, grid_color, rect, width)
                    Grid_num.draw()

                    Grid_counter += 1
            
            else:
                for x in range(9, -1, order):
                    Grid_num = SimpleText.SimpleText(self.surface, [x*self.grid_size + self.left_margin + width, y*self.grid_size + self.top_margin + width], str(Grid_counter), num_color, num_size)
                    rect = pygame.Rect(x*self.grid_size + self.left_margin, y*self.grid_size + self.top_margin, self.grid_size, self.grid_size)
                
                    pygame.draw.rect(self.surface, grid_color, rect, width)
                    Grid_num.draw()

                    Grid_counter += 1
            order *= -1

    def X_pos(self, grid_num):

        #return x coordinate in the center of said grid.
        #return None if value is invalid.

        if type(grid_num) != int or grid_num <= 0 or grid_num > 100:
            return None

        if ((grid_num - 1) // 10) % 2 == 0: # left --> right
            if grid_num % 10 == 0:
                return 9.5 * self.grid_size + self.left_margin
            else:
                return ((grid_num % 10) - 0.5) * self.grid_size + self.left_margin
        else: # right --> left
            if grid_num % 10 == 0:
                return 0.5 * self.grid_size + self.left_margin
            else:
                return (10.5 - (grid_num % 10)) * self.grid_size + self.left_margin

    def Y_pos(self, grid_num):

        #return y coordinate in the center of said grid.
        #return None if value is invalid.

        if type(grid_num) != int or grid_num <= 0 or grid_num > 100:
            return None
        
        return (9.5 - ((grid_num - 1) // 10)) * self.grid_size + self.top_margin


# Test.
if __name__ == "__main__":
    import pygame, sys

    pygame.init()
    pygame.display.set_caption("Ladder snake")

    # Game Variables
    Screen_Width = 600
    Screen_Height = 750

    screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    clock = pygame.time.Clock()

    grid_hold = pygame.Surface((600, 650))

    grid = Grid(grid_hold, 60, (0, 50))
    grid.drawGrid()


    #InGame
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

        screen.fill((0, 0, 0))
        
        # Drawing grid.
        screen.blit(grid_hold, (0, 0))
        block = pygame.Rect(grid.X_pos(77) - 2.5, grid.Y_pos(77) - 2.5, 5, 5)

        pygame.draw.circle(screen, [255, 255, 255], [grid.X_pos(60), grid.Y_pos(60)], 9)
        pygame.draw.rect(screen, [255, 255, 255], block)

        print(clock.get_fps())
        

        pygame.display.update()
        clock.tick(100)