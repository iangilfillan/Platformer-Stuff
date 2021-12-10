import time
import pygame
import random
import sys
import os
import re
from collections import OrderedDict
import pathfinding_mod as pathfind
pygame.init()
class Window:
    run = True
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    clock = pygame.time.Clock()
    fps = 45
    tilesize = 48
    background_colour = (0, 0, 0)
    background_colour = (255, 255, 255)
    #fonts = {}
    types = OrderedDict(air = (255, 255, 255),
                        grass = (126, 200, 80),
                        water = (156, 211, 219),
                        rock = (155, 163, 164))
    can_save = False
    highlighted_tiles = []
    highlighting_rect = pygame.Rect(0, 0, tilesize * 2/3, tilesize * 2 / 3)

    def draw_window(self):
        tiles = self.tiles
        screen = self.screen
        screen.fill((255,255,255))
        count = 0
        drawing_rect = pygame.Rect(0, 0, self.tilesize, self.tilesize)
        for row_index, row in enumerate(tiles):
            for collumn_index, colour_index in enumerate(row):
                drawing_rect.x = collumn_index*self.tilesize
                drawing_rect.y = row_index*self.tilesize
                if type(colour_index) == str:
                    colour = (255, 255, 255)
                    pygame.draw.rect(screen, colour, drawing_rect)
                    text, wh = self.get_text(colour_index.capitalize(), colour = (212, 175, 55), fontsize = int(self.tilesize * 3 / 4))
                    w, h = wh
                    screen.blit(text, (drawing_rect.x + w / 3, drawing_rect.y + h / 6))
                else:
                    colour = list(self.types.values())[colour_index]
                    pygame.draw.rect(screen, colour, drawing_rect)
                count += 1
        drawing_rect = self.highlighting_rect
        for tile in self.highlighted_tiles:
            drawing_rect.x = tile[1] * self.tilesize + self.tilesize/ 6
            drawing_rect.y = tile[0] * self.tilesize + self.tilesize/ 6
            pygame.draw.rect(self.screen, (255, 0, 0, 50), drawing_rect)
        pygame.display.update()
    def step(self):
        self.clock.tick(self.fps)
        self.draw_window()
        self.get_events()
        if not self.run:
            pygame.quit()
            sys.exit()
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                self.keypress_inputs(event.key)
    def get_text(self, text, font = "arial", fontsize = 16, colour = (0, 0, 0)):
        """returns rendered text and a tuple of (text_width, text_height) assigns it to main class as a memo"""
        if "fonts" not in locals():
            self.fonts = {}
        if (font, fontsize) not in self.fonts:
            self.fonts[(font, fontsize)] = pygame.font.SysFont(font, fontsize)
        font = self.fonts[(font, fontsize)]

        return font.render(text, 1, colour), font.size(text)
    def keypress_inputs(self, key):
        if key == pygame.K_s:
            path = pathfind.pathfind(self.tiles)
            self.highlighted_tiles = path
def load_map():
    tiles = []
    with open("pathfinding.txt", "r") as File:
        lines = File.readlines()
    
    for line in lines:
        tiles.append([])
        matches = re.findall(r"\d|[ps]", line)
        for match in matches:
            if match.isalpha():
                tiles[-1].append(match)
            else:
                tiles[-1].append(int(match))
    return tiles
def main():
    global WIN
    WIN = Window()
    WIN.tiles = load_map()
    run = True
    while run:
        WIN.step()

if __name__ == "__main__":
    main()


