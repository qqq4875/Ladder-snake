import pygame, sys, Grid, Obstacle, random, Dice

def scale(image, size):
    return pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)


class Action:
    def __init__(self, 
                 display, 
                 grid, 
                 obstacle,
                 dice,
                 image_still, 
                 image_walk1, 
                 image_walk2,
                 image_climb1,
                 image_climb2,
                 image_eaten,
                 image_stuck,
                 image_slip):

        self.display = display
        self.grid = grid
        self.obstacle = obstacle
        self.dice = dice

        self.init_pos = 1
        self.cur_pos = 1
        self.tar_pos = 1
        self.init_pos_x = self.char_pos_x(self.init_pos)
        self.init_pos_y = self.char_pos_y(self.init_pos)
        self.cur_pos_x = self.char_pos_x(self.cur_pos)
        self.cur_pos_y = self.char_pos_y(self.cur_pos)
        self.tar_pos_x = self.char_pos_x(self.tar_pos)
        self.tar_pos_y = self.char_pos_y(self.tar_pos)
        self.char_size = (self.grid.grid_size, self.grid.grid_size)
        self.walking = False
        self.walked = True
        self.climbing = False
        self.eaten_up = False
        self.stucking = False
        self.slipping = False
        self.slip_found = False
        self.end_turn = True
        self.step_added = True
        self.win = False
        self.current_action_index = 0
        self.last_updated_image_index = pygame.time.get_ticks()
        self.action_image = None # For furher storage.

        self.still = scale(image_still, self.char_size)
        self.walk1 = scale(image_walk1, self.char_size)
        self.walk2 = scale(image_walk2, self.char_size)
        self.climb1 = scale(image_climb1, self.char_size)
        self.climb2 = scale(image_climb2, self.char_size)
        self.eaten = scale(image_eaten, self.char_size)
        self.stuck = scale(image_stuck, self.char_size)
        self.slip = scale(image_slip, self.char_size)
        

    def char_pos_x(self, grid_num):
        return self.grid.X_pos(grid_num) - self.grid.grid_size / 2
    

    def char_pos_y(self, grid_num):
        return self.grid.Y_pos(grid_num) - self.grid.grid_size / 2


    def update_action(self):
        current_time = pygame.time.get_ticks()
        # check if time has passed enough to change action image.
        if current_time - self.last_updated_image_index > 250:
            self.last_updated_image_index = current_time
            self.current_action_index = (self.current_action_index + 1) % 2


    def check_action(self):
        
        # Flip the image.
        if self.cur_pos in range(11, 21) or self.cur_pos in range(31, 41) or self.cur_pos in range(51, 61) or self.cur_pos in range(71, 81) or self.cur_pos in range(91, 101):
            if self.walking:
                if self.current_action_index == 0:
                    self.action_image = pygame.transform.flip(self.walk1, flip_x=True, flip_y=False)
                else:
                    self.action_image = pygame.transform.flip(self.walk2, flip_x=True, flip_y=False)

            elif self.slipping:
                self.action_image = pygame.transform.flip(self.slip, flip_x=True, flip_y=False)

        else:
            if self.walking:
                if self.current_action_index == 0:
                    self.action_image = self.walk1
                else:
                    self.action_image = self.walk2

            elif self.slipping:
                self.action_image = self.slip

        if self.climbing:
            if self.current_action_index == 0:
                self.action_image = self.climb1
            else:
                self.action_image = self.climb2

        elif self.eaten_up:
            self.action_image = self.eaten

        elif self.stucking:
            self.action_image = self.stuck

        elif not self.walking and not self.climbing and not self.slipping and not self.stucking and not self.eaten_up:
            self.action_image = self.still
            self.end_turn = True


    def check_event(self):

        # check if walking or not.
        if self.cur_pos != self.tar_pos and not self.climbing and not self.eaten_up and not self.slipping and not self.walked:
            self.walking = True
            self.end_turn = False

        
        elif self.walking and self.cur_pos == self.tar_pos:
            self.walking = False

        # check if it is in the slippyfloor's square.
        for floor, length in self.obstacle.slippyfloor_pos.items():
            if not self.walking and 0 <= self.cur_pos - floor < length and not self.slip_found:
                self.slipping = True
                self.end_turn = False
                break

            if not self.walking and self.cur_pos == floor + length and self.slip_found:
                self.slipping = False
                self.slip_found = False
                break

        # check if it is in the ladder's bottom_end's square.
        if not self.walking and self.cur_pos in self.obstacle.ladder_pos.keys() and not self.slipping:
            self.climbing = True
            self.end_turn = False

        elif self.cur_pos in self.obstacle.ladder_pos.values():
            self.climbing = False

        # check if it is in the snake's head's square.
        if not self.walking and self.cur_pos in self.obstacle.snake_pos.keys() and not self.slipping:
            self.eaten_up = True
            self.end_turn = False

        elif self.cur_pos in self.obstacle.snake_pos.values():
            self.eaten_up = False

        if not self.walking and self.cur_pos in self.obstacle.hole_pos and not self.stucking and not self.end_turn and self.dice.dice_rolled:
            self.stucking = True

        elif self.stucking and self.end_turn: # <<<----
            self.stucking = False

        # check if character has already traveled to square 100
        if self.cur_pos == 100:
            self.win = True

        
    def move(self):

        self.update_action()

        self.check_event()

        self.check_action()

        if not self.win:

            if self.walking:
            
                # Stepping forward 1 square.
                if self.cur_pos_x == self.char_pos_x(self.cur_pos + 1) and self.cur_pos_y == self.char_pos_y(self.cur_pos + 1):
                    self.cur_pos += 1
                else:
                    self.cur_pos_x += (self.char_pos_x(self.cur_pos + 1) - self.char_pos_x(self.cur_pos)) / (self.grid.grid_size * 2) # Have to be divisible by grid_size
                    self.cur_pos_y += (self.char_pos_y(self.cur_pos + 1) - self.char_pos_y(self.cur_pos)) / (self.grid.grid_size * 2) # Have to be divisible by grid_size
            
                if self.cur_pos == self.tar_pos:

                    self.init_pos = self.tar_pos

                    self.tar_pos_x = self.char_pos_x(self.tar_pos)
                    self.tar_pos_y = self.char_pos_y(self.tar_pos)
                    self.init_pos_x = self.tar_pos_x
                    self.init_pos_y = self.tar_pos_y

                    self.walked = True
                
            elif self.climbing:

                for bottom_end, top_end in self.obstacle.ladder_pos.items():
                    if self.cur_pos == bottom_end:
                        self.tar_pos = top_end

                self.tar_pos_x = self.char_pos_x(self.tar_pos)
                self.tar_pos_y = self.char_pos_y(self.tar_pos)
            
                if self.cur_pos_x == self.tar_pos_x and self.cur_pos_y == self.tar_pos_y:
                    self.init_pos = self.tar_pos
                    self.cur_pos = self.tar_pos

                    self.init_pos_x = self.tar_pos_x
                    self.init_pos_y = self.tar_pos_y

                else:
                    self.cur_pos_x += (self.tar_pos_x - self.init_pos_x) / (self.grid.grid_size * 4) # Have to be divisible by grid_size
                    self.cur_pos_y += (self.tar_pos_y - self.init_pos_y) / (self.grid.grid_size * 4) # Have to be divisible by grid_size

            elif self.eaten_up:

                for head, tail in self.obstacle.snake_pos.items():
                    if self.cur_pos == head:
                        self.tar_pos = tail

                self.tar_pos_x = self.char_pos_x(self.tar_pos)
                self.tar_pos_y = self.char_pos_y(self.tar_pos)

                if self.cur_pos_x == self.tar_pos_x and self.cur_pos_y == self.tar_pos_y:
                    self.init_pos = self.tar_pos
                    self.cur_pos = self.tar_pos

                    self.init_pos_x = self.tar_pos_x
                    self.init_pos_y = self.tar_pos_y

                else:
                    self.cur_pos_x += (self.tar_pos_x - self.init_pos_x) / (self.grid.grid_size * 2) # Have to be divisible by grid_size
                    self.cur_pos_y += (self.tar_pos_y - self.init_pos_y) / (self.grid.grid_size * 2) # Have to be divisible by grid_size

            elif self.slipping:

                for floor, length in self.obstacle.slippyfloor_pos.items():
                    if 0 <= self.cur_pos - floor < length and not self.slip_found:
                        self.tar_pos = floor + length
                        self.slip_found = True
                        break

                self.tar_pos_x = self.char_pos_x(self.tar_pos)
                self.tar_pos_y = self.char_pos_y(self.tar_pos)

                # Stepping forward 1 square.
                if self.cur_pos_x == self.char_pos_x(self.cur_pos + 1) and self.cur_pos_y == self.char_pos_y(self.cur_pos + 1):
                    self.cur_pos += 1

                else:
                    self.cur_pos_x += (self.char_pos_x(self.cur_pos + 1) - self.char_pos_x(self.cur_pos)) / (self.grid.grid_size) # Have to be divisible by grid_size
                    self.cur_pos_y += (self.char_pos_y(self.cur_pos + 1) - self.char_pos_y(self.cur_pos)) / (self.grid.grid_size) # Have to be divisible by grid_size

                if self.cur_pos == self.tar_pos:
                    self.init_pos = self.tar_pos
                
                    self.init_pos_x = self.tar_pos_x
                    self.init_pos_y = self.tar_pos_y


        self.display.blit(self.action_image, (self.cur_pos_x, self.cur_pos_y))
        


    # called once.
    def roll_dice(self):
        
        self.walked = False
        self.step_added = False
        self.dice.roll_dice()


    def check_dice(self):

        if self.dice.dice_rolled and not self.step_added:
            #self.forward(self.dice.step)
            self.tar_pos += self.dice.step
            self.step_added = True

    

















class Character(Action):
    
    def __init__(self,
                 display, 
                 grid, 
                 obstacle,
                 dice,
                 image_still, 
                 image_walk1, 
                 image_walk2,
                 image_climb1,
                 image_climb2,
                 image_eaten,
                 image_stuck,
                 image_slip):
        super().__init__(display,
                         grid, 
                         obstacle,
                         dice,
                         image_still, 
                         image_walk1, 
                         image_walk2,
                         image_climb1,
                         image_climb2,
                         image_eaten,
                         image_stuck,
                         image_slip)
        

    def update_game(self):

        self.dice.update_dice_image()
        self.dice.draw_dice()
        self.move()
        self.check_dice()


        



            

            




        


# Test
if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((770, 770))
    pygame.display.set_caption("Ladder snake")
    clock = pygame.time.Clock()

    grid_hold = pygame.Surface((700, 700), pygame.SRCALPHA)

    grid = Grid.Grid(grid_hold, 70)
    grid.drawGrid()

    obstacle = Obstacle.Obstacle(screen, 
                        grid,
                        "Pygame_101/ladder.png",
                        "Pygame_101/snake.png",
                        "Pygame_101/hole.png",
                        "Pygame_101/ice.jpg")
    
    player_dice = Dice.Dice(screen, 
                    "Pygame_101/dice1.png",
                    "Pygame_101/dice2.png",
                    "Pygame_101/dice3.png",
                    "Pygame_101/dice4.png",
                    "Pygame_101/dice5.png",
                    "Pygame_101/dice6.png",
                    "Pygame_101/dice_rolling.png",
                    (200, 700),
                    (70, 70))
    

    bot_dice = Dice.Dice(screen, 
                    "Pygame_101/dice1.png",
                    "Pygame_101/dice2.png",
                    "Pygame_101/dice3.png",
                    "Pygame_101/dice4.png",
                    "Pygame_101/dice5.png",
                    "Pygame_101/dice6.png",
                    "Pygame_101/dice_rolling.png",
                    (400, 700),
                    (70, 70))

    
    player = Character(screen,
                    grid,
                    obstacle,
                    player_dice,
                    "Pygame_101/player-still.png",
                    "Pygame_101/player-walk1.png",
                    "Pygame_101/player-walk2.png",
                    "Pygame_101/player-climb1.png",
                    "Pygame_101/player-climb2.png",
                    "Pygame_101/player-eaten.png",
                    "Pygame_101/player-stuck.png",
                    "Pygame_101/player-slip.png")
    

    bot = Character(screen,
                    grid,
                    obstacle,
                    bot_dice,
                    "Pygame_101/bot-still.png",
                    "Pygame_101/bot-walk1.png",
                    "Pygame_101/bot-walk2.png",
                    "Pygame_101/bot-climb1.png",
                    "Pygame_101/bot-climb2.png",
                    "Pygame_101/bot-eaten.png",
                    "Pygame_101/bot-stuck.png",
                    "Pygame_101/bot-slip.png")
    
    
    
    
    obstacle.Ladder(10)
    obstacle.Snake(10)
    obstacle.Slippyfloor(15)
    obstacle.Hole(10)

    turn = 1
    turn_added = True

    game_ended = False

    while True:
        
        screen.fill("black")

        obstacle.spawn_slippyfloor()
        screen.blit(grid_hold, (0, 0))
        obstacle.spawn_hole()
        obstacle.spawn_ladder()
        obstacle.spawn_snake()

        player.update_game()
        bot.update_game()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_ended and event.key == pygame.K_SPACE and player.end_turn and not player.stucking and turn % 2 == 1 and player.dice.dice_rolled and player.walked and not bot.slipping and not bot.climbing and not bot.eaten_up:
                    player.roll_dice()
                    turn_added = False

        if not game_ended and bot.end_turn and not bot.stucking and turn % 2 == 0 and bot.dice.dice_rolled and bot.walked and not player.slipping  and not player.climbing and not player.eaten_up:
            bot.roll_dice()
            turn_added = False

        if player.stucking and bot.walked and turn % 2 == 1 and not bot.slipping and not bot.climbing and not bot.eaten_up:
            player.end_turn = True
            turn_added = False

        elif bot.stucking and player.walked and turn % 2 == 0 and not player.slipping and not player.climbing and not player.eaten_up:
            bot.end_turn = True
            turn_added = False

        # Determine whose turn it is.
        if not turn_added:
            if (not turn_added and player.walked and turn % 2 == 1): # <<------
                turn_added = True

            elif (not turn_added and bot.walked and turn % 2 == 0):
                turn_added = True

            if turn_added:
                turn += 1

        if player.win:
            winner = "Player"
            game_ended = True

        elif bot.win:
            winner = "bot"
            game_ended = True

        if game_ended:
            print(f"{winner} win!!")


        pygame.display.update()
        #clock.tick(90)

