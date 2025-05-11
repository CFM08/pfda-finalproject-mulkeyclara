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

        