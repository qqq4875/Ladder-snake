import pygame, sys, random, Grid, Obstacle, Dice, Action, SimpleText



def draw_button(screen, text, x, y, w, h, color, hover_color, text_size=30):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse_pos)

    pygame.draw.rect(screen, hover_color if is_hover else color, rect, border_radius=10)

    temp_font = pygame.font.SysFont(None, text_size, italic=True)
    text_surface = temp_font.render(text, True, (255, 255, 255))
    text_x = x + (w - text_surface.get_width()) // 2
    text_y = y + (h - text_surface.get_height()) // 2

    btn_text = SimpleText.SimpleText(screen, [text_x, text_y], text, [255, 255, 255], text_size)
    btn_text.draw()

    return is_hover and click[0] == 1


def show_menu_and_get_difficulty(screen):

    global selected_difficulty

    width, height = screen.get_width(), screen.get_height()

    screen.fill((30, 30, 45))

    title_text = "SELECT DIFFICULTY"
    temp_font = pygame.font.SysFont(None, 50, italic=True)
    title_surface = temp_font.render(title_text, True, (255, 255, 255))
    title_x = (width - title_surface.get_width()) // 2

    title = SimpleText.SimpleText(screen, [title_x, 180], title_text, [255, 255, 255], 50)
    title.draw()

    btn_x = (width - 220) // 2
    if draw_button(screen, "Easy", btn_x, 280, 220, 50, (46, 139, 87), (60, 179, 113)):
        selected_difficulty = "EASY"

    elif draw_button(screen, "Medium", btn_x, 360, 220, 50, (218, 165, 32), (238, 232, 170)):
        selected_difficulty = "MEDIUM"

    elif draw_button(screen, "Hard", btn_x, 440, 220, 50, (178, 34, 34), (205, 92, 92)):
        selected_difficulty = "HARD"


def show_winner_screen(screen, winner_name):
    width, height = screen.get_width(), screen.get_height()

    screen.fill((20, 20, 30))

    temp_font_title = pygame.font.SysFont(None, 60, italic=True)
    t_surf = temp_font_title.render("GAME OVER!", True, (255, 215, 0))
    title = SimpleText.SimpleText(screen, [(width - t_surf.get_width()) // 2, 200], "GAME OVER!", [255, 215, 0], 60)
    title.draw()

    win_str = f"{winner_name} Wins!"
    temp_font_win = pygame.font.SysFont(None, 45, italic=True)
    w_surf = temp_font_win.render(win_str, True, (255, 255, 255))
    win_txt = SimpleText.SimpleText(screen, [(width - w_surf.get_width()) // 2, 280], win_str, [255, 255, 255], 45)
    win_txt.draw()

    btn_x = (width - 220) // 2

    if draw_button(screen, "Quit", btn_x, 460, 220, 50, (178, 34, 34), (205, 92, 92)):
        pygame.quit()
        sys.exit()




pygame.init()

screen = pygame.display.set_mode((700, 770))
pygame.display.set_caption("Ladder snake")
clock = pygame.time.Clock()

grid_hold = pygame.Surface((700, 700), pygame.SRCALPHA)

grid = Grid.Grid(grid_hold, 70, (0, 0))
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
                    (220, 700),
                    (70, 70))


bot_dice = Dice.Dice(screen, 
                    "Pygame_101/dice1.png",
                    "Pygame_101/dice2.png",
                    "Pygame_101/dice3.png",
                    "Pygame_101/dice4.png",
                    "Pygame_101/dice5.png",
                    "Pygame_101/dice6.png",
                    "Pygame_101/dice_rolling.png",
                    (420, 700),
                    (70, 70))


bot = Action.Character(screen,
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


player = Action.Character(screen,
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




turn = 1
turn_added = True

game_ended = False

# game sound effect.
roll_dice_sound = pygame.mixer.Sound("Pygame_101/roll_dice_sound.mp3")
eaten_up_sound = pygame.mixer.Sound("Pygame_101/eaten_up.mp3")
climbing_sound = pygame.mixer.Sound("Pygame_101/ladder.mp3")
slipping_sound = pygame.mixer.Sound("Pygame_101/slip.mp3")
stucking_sound = pygame.mixer.Sound("Pygame_101/Fall.mp3")


eaten_up_sound_played = True
climbing_sound_played = True
slipping_sound_played = True
stucking_sound_played = True


# text telling player.
player_turn_text = SimpleText.SimpleText(screen, (10, 725), "Your turn [SPACE] -->", (255, 255, 255))


# background music.
music_num = random.randint(1, 4)

if music_num == 1:
    pygame.mixer.music.load("Pygame_101/Music g1.mp3")
elif music_num == 2:
    pygame.mixer.music.load("Pygame_101/Music g2.mp3")
elif music_num == 3:
    pygame.mixer.music.load("Pygame_101/Music g3.mp3")
elif music_num == 4:
    pygame.mixer.music.load("Pygame_101/Music g4.mp3")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)


# difficulty
selected_difficulty = None

#In game.
while True:

    screen.fill("black")

    obstacle.spawn_slippyfloor()
    screen.blit(grid_hold, (0, 0))
    obstacle.spawn_hole()
    obstacle.spawn_ladder(15)
    obstacle.spawn_snake(60)

    player.update_game()
    bot.update_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_ended and selected_difficulty and event.key == pygame.K_SPACE and player.end_turn and not player.stucking and turn % 2 == 1 and player.dice.dice_rolled and player.walked and not bot.slipping and not bot.climbing and not bot.eaten_up:
                player.roll_dice()
                roll_dice_sound.play()
                turn_added = False

    if not game_ended and bot.end_turn and not bot.stucking and turn % 2 == 0 and bot.dice.dice_rolled and bot.walked and not player.slipping  and not player.climbing and not player.eaten_up:
        bot.roll_dice()
        roll_dice_sound.play()
        turn_added = False

    # Determine whose turn it is.
    if player.stucking and bot.walked and turn % 2 == 1 and not bot.slipping and not bot.climbing and not bot.eaten_up:
        player.end_turn = True
        turn_added = False

    elif bot.stucking and player.walked and turn % 2 == 0 and not player.slipping and not player.climbing and not player.eaten_up:
        bot.end_turn = True
        turn_added = False

    if not turn_added:
        if (not turn_added and player.walked and turn % 2 == 1):
            turn_added = True

        elif (not turn_added and bot.walked and turn % 2 == 0):
            turn_added = True

        if turn_added:
            turn += 1

    # text telling player that it is their turn.
    if turn % 2 == 1 and player.dice.dice_rolled and player.end_turn and (bot.end_turn or bot.stucking) and player.walked:
        player_turn_text.draw()


    # playing sound effect
    if (player.eaten_up or bot.eaten_up) and eaten_up_sound_played:
        eaten_up_sound.play()
        eaten_up_sound_played = False
    elif not eaten_up_sound_played and not player.eaten_up and not bot.eaten_up:
        eaten_up_sound_played = True

    if (player.climbing or bot.climbing) and climbing_sound_played:
        climbing_sound.play()
        climbing_sound_played = False
    elif not climbing_sound_played and not player.climbing and not bot.climbing:
        climbing_sound_played = True

    if (player.slipping or bot.slipping) and slipping_sound_played:
        slipping_sound.play()
        slipping_sound_played = False
    elif not slipping_sound_played and not player.slipping and not bot.slipping:
        slipping_sound_played = True

    if (player.stucking or bot.stucking) and stucking_sound_played:
        stucking_sound.play()
        stucking_sound_played = False
    elif (not stucking_sound_played and not player.stucking and not bot.stucking) or (not stucking_sound_played and player.stucking and bot.stucking):
        stucking_sound_played = True

    # game difficulty
    if selected_difficulty == None:
        show_menu_and_get_difficulty(screen)

        if selected_difficulty == "EASY":
            obstacle.Ladder(10)
            obstacle.Snake(4)
            obstacle.Slippyfloor(20, 2, 3)
            obstacle.Hole(4)

        elif selected_difficulty == "MEDIUM":
            obstacle.Ladder(5)
            obstacle.Snake(6)
            obstacle.Slippyfloor(15, 2, 4)
            obstacle.Hole(7)

        elif selected_difficulty == "HARD":
            obstacle.Ladder(3)
            obstacle.Snake(10)
            obstacle.Slippyfloor(15, 2, 4)
            obstacle.Hole(13)

    # who's winning
    if player.win:
        winner = "Player"
        game_ended = True

    elif bot.win:
        winner = "bot"
        game_ended = True

    if game_ended:
        show_winner_screen(screen, winner)
        #print(f"{winner} win!!")


    #print("walked:", player.walked)
    #print("slipping", player.slipping)
    #print("player end_turn", player.end_turn)
    #print("bot end_turn", bot.end_turn)
    #print("turn", turn)
    #print()
    pygame.display.update()
    #clock.tick(30)

