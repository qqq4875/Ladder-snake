import pygame, random, Grid, sys, math

class Obstacle:
    def __init__(self, display, grid):
        self.display = display
        self.grid = grid
        self.ladder_pos = {} # Contain integer grid number for each ladder's end as key: value pair (bottom_end: top_end).
        self.snake_pos = {} # Contain integer grid number for each snake's end as key: value pair (head: tail).
        self.hole_pos = [] # Contain integer grid number of each holes.
        self.slippyfloor = {} # Contain integer grid number of the first floor to spawn and length of the floor as key: value pair.


    def ladder(self, amount=0):

        self.ladder_pos = {} # Set clear if recalled.
        
        for time in range(amount):
            bottom_end = random.randint(5, 80) # bottom_end can only be spawned in square 5 - 80
            # Check if the bottom_end already exist or is in the same grid as snake's head.
            while bottom_end in self.ladder_pos.keys() or bottom_end in self.snake_pos.keys():
                bottom_end = random.randint(5, 80)

            top_end = random.randint(10, 99) # top_end can only be spawned in square 10 - 99
            # Check if top_end in the same or less row as bottom_end, and if they are atleast 5 grids apart.
            while top_end // 10 <= bottom_end // 10 or (top_end // 10 == (bottom_end // 10) + 1 and top_end % 10 - bottom_end % 10 < 5):
                top_end = random.randint(10, 99)

            self.ladder_pos.update({bottom_end: top_end})


    def spawn_ladder(self, image_file, ladder_width=10):
        
        ladder_org = pygame.image.load(image_file)

        for bottom_end, top_end in self.ladder_pos.items():

            Y_dist = -(self.grid.Y_pos(top_end) - self.grid.Y_pos(bottom_end)) # Top position is less than bottom.
            X_dist = self.grid.X_pos(top_end) - self.grid.X_pos(bottom_end)
            angle = math.degrees(math.atan2(Y_dist, X_dist)) - 90

            ladder_scaled = pygame.transform.scale(ladder_org, (ladder_width, math.sqrt(Y_dist**2 + X_dist**2)))
            ladder_rot = pygame.transform.rotate(ladder_scaled, angle)

            if X_dist < 0: # bottom_end is further down the axis.
                center = ladder_rot.get_rect(center = (self.grid.X_pos(bottom_end) - (abs(X_dist) / 2), self.grid.Y_pos(bottom_end) - (Y_dist / 2)))
            else:
                center = ladder_rot.get_rect(center = (self.grid.X_pos(top_end) - (abs(X_dist) / 2), self.grid.Y_pos(bottom_end) - (Y_dist / 2)))

            self.display.blit(ladder_rot, center)






# Test.
if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    grid = Grid.Grid(screen)
    obstacle = Obstacle(screen, grid)

    obstacle.ladder(40)

    while True:
        
        screen.fill("black")

        grid.drawGrid()
        obstacle.spawn_ladder("Pygame_101/ladder.png")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

        pygame.display.update()
        clock.tick(30)



            
