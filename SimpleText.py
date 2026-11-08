# SimpleText class
import pygame, sys
from pygame.locals import *
class SimpleText():
  def __init__(self, window, loc, value, textColor, textSize=30):
    pygame.font.init()
    self.window = window
    self.loc = loc
    self.font = pygame.font.SysFont(None, textSize, italic=True)
    self.textColor = textColor
    self.text = None # so that the call to setText below will
    # force the creation of the text image
    self.setValue(value) # set the initial text for drawing
  def setValue(self, newText):
    if self.text == newText:
      return # nothing to change
    self.text = newText # save the new text
    self.textSurface = self.font.render(self.text, True, self.textColor) # <-- Surface
  def draw(self):
    self.window.blit(self.textSurface, self.loc)


# Test.
if __name__ == "__main__":

  pygame.init()

  screen = pygame.display.set_mode((500, 500))

  Text = SimpleText(screen, [250, 250], "Test text.", [255, 255, 255])

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit
        sys.exit()

    screen.fill([0, 0, 0])

    Text.draw()

    pygame.display.update()



        