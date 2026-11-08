import pygame, sys, Grid, Obstacle, Action, random

def scale(image, size):
    return pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)

class Dice:
    def __init__(self,
                 display,
                 image_dice_1,
                 image_dice_2,
                 image_dice_3,
                 image_dice_4,
                 image_dice_5,
                 image_dice_6,
                 image_dice_rolling,
                 dice_position=(0, 0),
                 dice_size=(0, 0)):
        
        self.display = display
        self.dice_pos = dice_position
        self.dice_size = dice_size
        self.dice_1 = scale(image_dice_1, self.dice_size)
        self.dice_2 = scale(image_dice_2, self.dice_size)
        self.dice_3 = scale(image_dice_3, self.dice_size)
        self.dice_4 = scale(image_dice_4, self.dice_size)
        self.dice_5 = scale(image_dice_5, self.dice_size)
        self.dice_6 = scale(image_dice_6, self.dice_size)
        self.dice_rolling = scale(image_dice_rolling, self.dice_size)
        self.dice_image = self.dice_1 # For further changes.
        self.rolling = False
        self.step = 0
        self.dice_rolled = True
        self.previous_step = 0
        self.amount_rolled_each_turn = 5
        self.dice_num = 1
        self.dice_image_index = 0
        self.last_dice_image_index = pygame.time.get_ticks()


    def draw_dice(self):

        self.display.blit(self.dice_image, self.dice_pos)


    def update_dice_image_index(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dice_image_index > 180:
            self.last_dice_image_index = current_time
            self.dice_image_index = (self.dice_image_index + 1) % 2


    def update_dice_image(self):

        self.update_dice_image_index()

        # Rolling.
        if self.rolling and self.dice_image == self.dice_rolling and self.dice_image_index == 1:
            self.amount_rolled_each_turn -= 1
        
        # Last roll to determine the step.
        if self.amount_rolled_each_turn == 0:

            if self.dice_num == 1:
                self.dice_image = self.dice_1
            elif self.dice_num == 2:
                self.dice_image = self.dice_2
            elif self.dice_num == 3:
                self.dice_image = self.dice_3
            elif self.dice_num == 4:
                self.dice_image = self.dice_4
            elif self.dice_num == 5:
                self.dice_image = self.dice_5
            elif self.dice_num == 6:
                self.dice_image = self.dice_6

            self.rolling = False

        # In between rolling.
        if self.rolling and self.dice_image_index == 1 and self.amount_rolled_each_turn > 0 and self.dice_num != 0:
            if self.dice_num == 1:
                self.dice_image = self.dice_1
            elif self.dice_num == 2:
                self.dice_image = self.dice_2
            elif self.dice_num == 3:
                self.dice_image = self.dice_3
            elif self.dice_num == 4:
                self.dice_image = self.dice_4
            elif self.dice_num == 5:
                self.dice_image = self.dice_5
            elif self.dice_num == 6:
                self.dice_image = self.dice_6

        elif self.rolling and self.dice_image_index == 0:
            self.dice_image = self.dice_rolling
            self.dice_num = random.randint(1, 6)




        # Rolled.
        if not self.rolling and self.amount_rolled_each_turn == 0:

            self.step = self.dice_num
            self.amount_rolled_each_turn = 5
            self.dice_rolled = True




    def roll_dice(self):

        self.dice_num = random.randint(1, 6)
        self.rolling = True
        self.dice_rolled = False


    




# Test
if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    grid_holder = pygame.Surface((600, 600), pygame.SRCALPHA)

    grid = Grid.Grid(grid_holder)
    grid.drawGrid()

    obstacle = Obstacle.Obstacle(screen, 
                        grid,
                        "Pygame_101/ladder.png",
                        "Pygame_101/arrow.png",
                        "Pygame_101/hole.png",
                        "Pygame_101/ice.jpg")
    
    dice = Dice(screen,
                    "Pygame_101/1.png",
                    "Pygame_101/2.png",
                    "Pygame_101/3.png",
                    "Pygame_101/4.png",
                    "Pygame_101/5.webp",
                    "Pygame_101/6.png",
                    "Pygame_101/7.png",
                    (200, 200),
                    (50, 50))


    while True:
        
        screen.fill("black")

        
        

        #player.spawn_player()
        #player.move()
        #if not player.stucking:
            #pass # Roll the dice
        
        #else:
            #pass

        #print(pygame.time.get_ticks())

        #for event in pygame.event.
        dice.update_dice_image()
        dice.draw_dice()
        print(dice.step)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice.role_dice()

        pygame.display.update()
        clock.tick(60)
