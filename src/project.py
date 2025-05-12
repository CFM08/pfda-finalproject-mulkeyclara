import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 1200, 600
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
    (255, 0, 255), #magenta
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

def show_message(screen, text, y_offset=0, size=60):
      font = pygame.font.SysFont(None, size)
      render = font.render(text, True, (255, 255, 255))
      rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
      screen.blit(render, rect)

def start_new_round(state):
      state['round'] += 1
      if state['round'] > state['max_rounds']:
            state['confetti'] = [ConfettiParticle() for _ in range(100)]
            state['game_state'] = "win"
            return
      state['sequence'].append(random.randint(0, 8))
      state['user_sequence'] = []
      state['flashing'] = True
      state['flash_index'] = 0
      state['flash_timer'] = pygame.time.get_ticks()

class ConfettiParticle:
      def __init__(self):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(-HEIGHT, 0)
            self.size = random.randint(4, 8)
            self.speed_y = random.uniform(1, 4)
            self.speed_x = random.uniform(-1, 1)
            self.color = random.choice(COLORS)

      def update(self):
            self.y += self.speed_y
            self.x += self.speed_x
            if self.y > HEIGHT:
                  self.y = random.randint(-HEIGHT, 0)
                  self.x = random.randint(0, WIDTH)

      def draw(self, screen):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

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
            'flash_delay' : 650,
            'round': 0,
            'max_rounds': 10,
            'click_highlight': None,
            'click_time': 0,
            'click_duration': 250,
            'waiting_to_continue': False,
            'continue_time': 0,
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
                 highlight = None

                 if state['flashing'] and state['flash_index'] < len(state['sequence']):
                       highlight = state['sequence'][state['flash_index']]

                 elif state['click_highlight'] is not None:
                       if now - state['click_time'] < state['click_duration']:
                             highlight = state['click_highlight']
                       else:
                             state['click_highlight'] = None
                
                 draw_grid(screen, highlight)

                 if state['waiting_to_continue']:
                       if now - state['click_time'] > state['click_duration']:
                              state['waiting_to_continue'] = False
                              start_new_round(state)

                 show_message(screen, f"Round:{state['round']}", y_offset=-280, size=30)
                 show_message(screen, f"Score: {len(state['sequence']) - 1}", y_offset=-250, size=30)
            
            elif state['game_state'] == GAME_OVER:
                  screen.fill((0, 0, 0)) # to black out the screen
                  show_message(screen, "Game Over!", y_offset = 0, size=60)
                  show_message(screen, f"Score: {len(state['sequence']) - 1}", y_offset=-45, size=40)
                  show_message(screen, "Click To Restart!", y_offset=120, size=25)
            
            elif state['game_state'] == "win":
                  screen.fill((0, 0, 0))
                  for particle in state.get('confetti', []):
                        particle.update()
                        particle.draw(screen)
                  show_message(screen, "You Win!", y_offset = 0, size=60)
                  show_message(screen, f"Score: {len(state['sequence']) - 1}", y_offset=-45, size=40)
                  show_message(screen, "Click To Play Again!", y_offset=120, size=25)

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

                          state['click_highlight'] = tile
                          state['click_time'] = pygame.time.get_ticks()

                          index = len(state['user_sequence']) - 1
                          if tile != state['sequence'][index]:
                                state['game_state'] = GAME_OVER
                          elif len(state['user_sequence']) == len(state['sequence']):
                                state['waiting_to_continue'] = True
                                state['continue_time'] = pygame.time.get_ticks()
                    
                    elif state['game_state'] == GAME_OVER or state['game_state'] == "win":
                          state['sequence'] = []
                          state['user_sequence'] = []
                          state['round'] = 0
                          state['confetti'] = []
                          state['game_state'] = START

      while running:
            
            clock.tick(60)
           
            pygame.quit()
      
if __name__ == "__main__":
      main()
