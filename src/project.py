import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Memorization")
TILE_SIZE = WIDTH // 3

COLORS = [
    (255, 0, 0), #red
    (0, 255, 0), #green
    (0, 0, 255), #blue
    (0, 255, 255), #cyan
    (255, 255, 0), #yellow
    (0, 126, 126), #teal
    (130, 0, 130), #purple
    (255, 0, 265), #magenta
    (255, 168, 0), #orange
]

START, PLAYING, GAME_OVER = "start", "playing", "game_over"

def draw_grid(screen, highlight=None):
    for i in range (9):
        row = i // 3
        col = i % 3
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        color = COLORS[i]
        if highlight == i:
            color = tuple(min(255, c + 100) for c in color) # brightening
        pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (0, 0 , 0), (x, y, TILE_SIZE, TILE_SIZE), 3)

def get_tile_from_pos(pos):
            x, y = pos
            col = x //TILE_SIZE
            row = y // TILE_SIZE
            return row * 3 + col

def show_message(screen, text):
      font = pygame.font.SysFont(None, 60)
      render = font.render(text, True, (255, 255, 255))
      rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
      screen.blit(render, rect)

def start_new_round(state):
      state['sequence'].append(random.randint(0, 8))
      state['user_sequence'] = []
      state['flashing'] = True
      state['flash_index'] = 0
      state['flash_timer'] = pygame.time.get_ticks()

def main():
      screen = pygame.display.set_mode((WIDTH, HEIGHT))
      pygame.display.set_caption("Color Memory Game")
      clock = pygame.time.Clock()

      state = {
            'game_state' : START,
            'sequence' : [],
            'user_sequence' : [],
            'flashing' : False,
            'flash_index' : 0,
            'flash_timer' : 0,
            'flash_delay' : 650
      }

      running = True
      while running:
            screen.fill((30, 30, 30))
            now = pygame.time.get_ticks()

            if state['game_state'] == START:
                  show_message(screen, "Click to Start")

            elif state['game_state'] == PLAYING:
                 if state['flashing']:
                     if now - state['flash_timer'] > state['flash_delay']:
                             state['flash_timer'] = now
                             state['flash_index'] += 1
                             if state['flash_index'] >= len(state['sequence']):
                                state['flashing'] = False
                 highlight =(
                      state['sequence'][state['flash_index']]
                      if state['flashing'] and state['flash_index'] < len(state['sequence'])
                      else None
                )
                 draw_grid(screen, highlight)
            
            pygame.display.flip()

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        running = False

                  elif event.type == pygame.MOUSEBUTTONDOWN:
                    if state['game_state'] == START:
                          state['sequence'] = []
                          start_new_round(state)
                          state['game_state'] = PLAYING

                    elif state['game_state'] == PLAYING and not state['flashing']:
                          tile = get_tile_from_pos(event.pos)
                          state['user_sequence'].append(tile)

                          if tile != state['sequence'][len(state['sequence']) - 1]:
                                state['game_state'] = GAME_OVER
                          elif len(state['user_sequence']) == len(state['sequence']):
                                pygame.time.delay(500)
                                start_new_round(state)
                    
                    elif state['game_state'] == GAME_OVER:
                          state['game_state'] = START

      while running:
            
            clock.tick(60)
           
            pygame.quit()
      
if __name__ == "__main__":
      main()
