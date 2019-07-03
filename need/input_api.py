import pygame, pygame.event, pygame.draw, string
from pygame.locals import *
def get_key():  #once time get a key
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    elif event.type==QUIT:
      return pygame.quit()

def display_box(screen, message):
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),  #input color
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255), #message color
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen):
  current_string = []
  display_box(screen, "Name" + ": " + ''.join(current_string))
  while 1:  #listening keyborad event
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, "Name" + ": " + ''.join(current_string))
  return ''.join(current_string)

def model_input(screen):
    return ask(screen)

if __name__ == '__main__': model_input()
