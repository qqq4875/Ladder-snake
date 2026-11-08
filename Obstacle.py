import pygame, random, Grid, sys, math

class Obstacle:
    def __init__(self, display, grid, ladder, snake, hole, slippyfloor):
        self.display = display
        self.grid = grid
        self.ladder = pygame.image.load(ladder).convert_alpha()
        self.snake = pygame.image.load(snake).convert_alpha()
        self.hole = pygame.image.load(hole).convert_alpha()
        self.slippyfloor = pygame.image.load(slippyfloor).convert_alpha()

        self.ladder_pos = {} # Contain integer grid number for each ladder's end as key: value pair (bottom_end: top_end).
        self.snake_pos = {} # Contain integer grid number for each snake's end as key: value pair (head: tail).
        self.hole_pos = [] # Contain integer grid number of each holes.
        self.slippyfloor_pos = {} # Contain integer grid number of the first floor to spawn and length of the floor as key: value pair.


    def Ladder(self, amount=0):

        self.ladder_pos.clear() # Set clear if recalled.
        
        for time in range(amount):
            
            while True:

                bottom_end = random.randint(5, 80) # bottom_end can only be spawned in square 5 - 80.

                # Check if the bottom_end already exist or is in the same grid as snake's head or hole.
                if bottom_end not in self.ladder_pos.keys() and bottom_end not in self.snake_pos.keys() and bottom_end not in self.hole_pos:
                    break

            while True:

                top_end = random.randint(11, 99)

                # Check if top_end is in more row than bottom_end, and if they are atleast 5 grids apart.
                if (top_end - 1) // 10 > (bottom_end - 1) // 10 and top_end - bottom_end >= 5:
                    break

            self.ladder_pos.update({bottom_end: top_end})


    def Snake(self, amount=0):

        self.snake_pos.clear() # Set clear if recalled.
        
        for time in range(amount):

            while True:

                head = random.randint(11, 99) # head can only be spawned in square 11 - 99.

                # Check if the head position already exist or is in the same grid as ladder's bottom_end or hole.
                if head not in self.snake_pos.keys() and head not in self.ladder_pos.keys() and head not in self.hole_pos:
                    break

            tail = random.randint(5, 80) # tail can only be spawned in square 5 - 80.
            
            while True:
                
                tail = random.randint(5, 80) # tail can only be spawned in square 5 - 80.

                # Check if the head position is in more row than tail position, and if they are atleast 5 grids apart.
                if (head - 1) // 10 > (tail - 1) // 10 and head - tail >= 5:
                    break

            self.snake_pos.update({head: tail})

    
    def Hole(self, amount=0):

        self.hole_pos.clear # Set clear if recalled.

        for time in range(amount):

            while True:

                hole_clip = False

                Hole = random.randint(2, 99) # holes can only be spawn in square 2 - 99.

                for floor, length in self.slippyfloor_pos.items():
                    if Hole >= floor and Hole - floor < length:
                        hole_clip = True
                
                # Check if the hole position already exist or is in the same square as ladder's bottom_end or snake's head or slippyfloors.
                if Hole not in self.hole_pos and Hole not in self.ladder_pos.keys() and Hole not in self.snake_pos.keys() and not hole_clip:
                    self.hole_pos.append(Hole)
                    break


    def Slippyfloor(self, amount=0, min_length=2, max_length=3):

        self.slippyfloor_pos.clear() # Set clear if recalled.

        for time in range(amount):

            # Check if the dict "slippyfloor_pos" is empty.
            if len(self.slippyfloor_pos) == 0:

                while True:

                    hole_clip = False

                    n_slip_flo = random.randint(2, 90 - max_length) # slippyfloor can only be spawn in square 2 - 90.
                    n_length = random.randint(min_length, max_length)

                    # Check if hole is within slippyfloor's length.
                    for hole in self.hole_pos:
                        if hole >= n_slip_flo and hole - n_slip_flo < n_length:
                            hole_clip = True
                
                    if not hole_clip:
                        self.slippyfloor_pos.update({n_slip_flo: n_length})
                        break


            else:

                while True:

                    hole_clip = False
                    floor_clip = False

                    n_slip_flo = random.randint(2, 90 - max_length) # slippyfloor can only be spawn in square 2 - 90.
                    n_length = random.randint(min_length, max_length)

                    # Check if hole is within slippyfloor's length.
                    for hole in self.hole_pos:
                        if hole >= n_slip_flo and hole - n_slip_flo < n_length:
                            hole_clip = True
                    
                    # Check if the slippyfloor position already exist or is within 2 grids apart from nearest slippy floors.
                    for slip_flo, length in self.slippyfloor_pos.items():
                        if (n_slip_flo > slip_flo and n_slip_flo - (slip_flo + length-1) <= 2) or (n_slip_flo < slip_flo and slip_flo - (n_slip_flo + n_length-1) <= 2):
                            floor_clip = True

                    if not hole_clip and not floor_clip:
                        self.slippyfloor_pos.update({n_slip_flo: n_length})
                        break


    def spawn_ladder(self, ladder_width=10):
        
        ladder_org = self.ladder

        for bottom_end, top_end in self.ladder_pos.items():

            Y_dist = -(self.grid.Y_pos(top_end) - self.grid.Y_pos(bottom_end)) # Top position is less than bottom.
            X_dist = self.grid.X_pos(top_end) - self.grid.X_pos(bottom_end)
            angle = math.degrees(math.atan2(Y_dist, X_dist)) - 90 # For if ladder is H instead of II.

            ladder_scaled = pygame.transform.scale(ladder_org, (ladder_width, math.sqrt(Y_dist**2 + X_dist**2)))
            ladder_rot = pygame.transform.rotate(ladder_scaled, angle)

            if X_dist < 0: # bottom_end is further down the axis.
                center = ladder_rot.get_rect(center = (self.grid.X_pos(bottom_end) - (abs(X_dist) / 2), self.grid.Y_pos(bottom_end) - (Y_dist / 2)))
            else:
                center = ladder_rot.get_rect(center = (self.grid.X_pos(top_end) - (abs(X_dist) / 2), self.grid.Y_pos(bottom_end) - (Y_dist / 2)))

            self.display.blit(ladder_rot, center)


    def spawn_snake(self, snake_width=20):
        
        snake_org = self.snake

        for head, tail in self.snake_pos.items():

            Y_dist = -(self.grid.Y_pos(head) - self.grid.Y_pos(tail)) # The head position is less than bottom.
            X_dist = self.grid.X_pos(head) - self.grid.X_pos(tail)
            angle = math.degrees(math.atan2(Y_dist, X_dist)) - 90 # For if snake is pointing upword.

            snake_scaled = pygame.transform.scale(snake_org, (snake_width, math.sqrt(Y_dist**2 + X_dist**2)))
            snake_rot = pygame.transform.rotate(snake_scaled, angle)

            if X_dist < 0: # tail is further down the axis.
                center = snake_rot.get_rect(center = (self.grid.X_pos(tail) - (abs(X_dist) / 2), self.grid.Y_pos(tail) - (Y_dist / 2)))
            else:
                center = snake_rot.get_rect(center = (self.grid.X_pos(head) - (abs(X_dist) / 2), self.grid.Y_pos(tail) - (Y_dist / 2)))

            self.display.blit(snake_rot, center)

    
    def spawn_hole(self):

        hole_org = self.hole
        hole_scaled = pygame.transform.scale(hole_org, (self.grid.grid_size, self.grid.grid_size))

        for hole in self.hole_pos:
            position = (self.grid.X_pos(hole) - self.grid.grid_size / 2, self.grid.Y_pos(hole) - self.grid.grid_size / 2)
            self.display.blit(hole_scaled, position)


    def spawn_slippyfloor(self):

        slip_flo = self.slippyfloor
        slip_flo_scaled = pygame.transform.scale(slip_flo, (self.grid.grid_size, self.grid.grid_size))

        for floor, length in self.slippyfloor_pos.items():
            for time in range(length):
                position = (self.grid.X_pos(floor) - self.grid.grid_size / 2, self.grid.Y_pos(floor) - self.grid.grid_size / 2)
                self.display.blit(slip_flo_scaled, position)
                floor += 1




# Test.
if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((630, 630))
    clock = pygame.time.Clock()

    grid_hold = pygame.Surface((630, 630), pygame.SRCALPHA)

    grid = Grid.Grid(grid_hold, 60, (30, 30))
    grid.drawGrid()

    obstacle = Obstacle(screen,
                        grid,
                        "Pygame_101/ladder.png",
                        "Pygame_101/arrow.png",
                        "Pygame_101/hole.png",
                        "Pygame_101/ice.jpg")

    obstacle.Ladder(4)
    obstacle.Snake(5)
    obstacle.Slippyfloor(6)
    obstacle.Hole(10)

    screen.fill("black")

    while True:

        print(clock.get_fps())

        obstacle.spawn_slippyfloor()
        screen.blit(grid_hold, (0, 0))
        obstacle.spawn_hole()
        obstacle.spawn_ladder()
        obstacle.spawn_snake()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

        pygame.display.update()
        clock.tick(0)



            
