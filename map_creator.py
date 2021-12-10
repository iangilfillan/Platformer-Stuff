import time
import pygame
import random
import sys
import os
if os.getcwd() == "Saves":
    path = path = os.path.join("\\Users","User","Documents","Python Saves","Fun Projects","Tier_1","current","platformer_stuff")
    os.chdir(path)

pygame.init()    
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
TILESIZE = 32

FONTS = {}

def get_text(text, font = "arial", fontsize = 16):
    if (font, fontsize) not in FONTS:
        FONTS[(font, fontsize)] = pygame.font.SysFont(font, fontsize)
    font = FONTS[(font, fontsize)]


    return font.render(text, 1, (0, 0, 0)), font.size(text)
    #text_width, text_height = font.size(text)
    #text = font.render(text)

    #return text, (text_width, text_height)


def create_tiles():
    tiles = []
    for x in range(WIDTH // TILESIZE):
        tiles.append([])
        for y in range(HEIGHT // TILESIZE):
            tiles[x].append(None)
    return tiles

def draw_window(tiles):
    WIN.fill((255, 255, 255))
    Tile = pygame.Rect(0, 0, TILESIZE - 2, TILESIZE - 2)
    count = 0
    for row_index, row in enumerate(tiles):
        for collumn_index, tiles in enumerate(row):
            Tile.x = row_index * TILESIZE
            Tile.y = collumn_index * TILESIZE

            txt, txt_wh = get_text(str(count))
            txt_w, txt_h = txt_wh

            pygame.draw.rect(WIN, (64, 128, 64), Tile)
            WIN.blit(txt, (Tile.x, Tile.y))
            count += 1

    pygame.display.update()
def main():
    run = True
    clock = pygame.time.Clock()
    tiles = create_tiles()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        draw_window(tiles)
main()
