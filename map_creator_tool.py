import time
import pygame
import random
import sys
import os
import re
from collections import OrderedDict
pygame.init()
class Window:
    run = True
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    clock = pygame.time.Clock()
    fps = 45
    tilesize = 8
    background_colour = (0, 0, 0)
    background_colour = (255, 255, 255)
    fonts = {}
    types = OrderedDict(air = (255, 255, 255),
                        grass = (126, 200, 80),
                        water = (156, 211, 219),
                        rock = (155, 163, 164))
    can_save = False
    selected_points = [(), ()]
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
                    text, _ = self.get_text(colour_index.capitalize(), colour = (212, 175, 55), fontsize = 32)
                    screen.blit(text, (drawing_rect.x, drawing_rect.y))
                else:
                    colour = list(self.types.values())[colour_index]
                    pygame.draw.rect(screen, colour, drawing_rect)
                count += 1

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = x // self.tilesize, y // self.tilesize
                x, y = round(x), round(y)
                self.selected_points[0] = x, y
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                x, y = x // self.tilesize, y // self.tilesize
                x, y = round(x), round(y)
                self.selected_points[1] = x, y
                indexes = select_area(self.tiles, self.selected_points[0], self.selected_points[1])
                print(indexes)
        if pygame.mouse.get_pressed()[0]:
            point2 = pygame.mouse.get_pos()
            x, y = self.selected_points[0]
            x, y = x // self.tilesize * self.tilesize, y // self.tilesize * self.tilesize
            outline_area(self.tiles, (x * self.tilesize, y * self.tilesize), point2)
            pygame.display.update()
        self.keyheld_inputs()
    def get_text(self, text, font = "arial", fontsize = 16, colour = (0, 0, 0)):
        if (font, fontsize) not in self.fonts:
            self.fonts[(font, fontsize)] = pygame.font.SysFont(font, fontsize)
        font = self.fonts[(font, fontsize)]

        return font.render(text, 1, colour), font.size(text)
    def keypress_inputs(self, key):
        tiles = self.tiles
        pressed = pygame.key.get_pressed()
        if key == pygame.K_s and pressed[pygame.K_LALT] and self.can_save:
            save_map(tiles)
            print("saved")
        elif key == pygame.K_l:
            self.can_save = True
            self.tiles = load_map()
    def keyheld_inputs(self):
        tiles = self.tiles
        keys = pygame.key.get_pressed()
        options = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3]
        for key in options:
            if keys[key] and keys[pygame.K_LALT] == 0:
                place_tile(tiles, key, pygame.mouse.get_pos())
                break
        options = [pygame.K_p, pygame.K_s]
        for key in options:
            if keys[key] and keys[pygame.K_LALT] == 0:
                place_mob(tiles, key, pygame.mouse.get_pos())
def save_map(tiles):
    tiles = tiles
    string = ""
    for row in tiles:
        string += f"{row}"
        string += "\n"
    with open("current_save.txt", "w") as File:
        File.write(string)
def load_map():
    tiles = []
    with open("current_save.txt", "r") as File:
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
def create_tiles():
    tiles = []
    for row in range(WIN.height // WIN.tilesize):
        tiles.append([])
        for _ in range(WIN.width // WIN.tilesize):
            tiles[row].append(0)
    return tiles
def place_tile(tiles, key, mouse_pos):
    index = key - 48
    if index > len(WIN.types) - 1:
        return
    x, y = mouse_pos
    x = x // WIN.tilesize
    y = y // WIN.tilesize
    x = round(x)
    y = round(y)
    tiles[y][x] = index

def place_mob(tiles, key, mouse_pos):
    placement = "0"
    if key == pygame.K_p:
        placement = "p"
    elif key == pygame.K_s:
        placement = "s"
    x, y = mouse_pos
    x = x // WIN.tilesize
    y = y // WIN.tilesize
    x = round(x)
    y = round(y)
    tiles[y][x] = placement

def select_area(tiles, point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    l_tiles = []
    
def outline_area(tiles, point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    colour = (0, 0, 0)
    pygame.draw.line(WIN.screen, colour, (x1, y1), (x1, y2)) #1 vertical
    pygame.draw.line(WIN.screen, colour, (x2, y1), (x2, y2)) #2 -*vertical
    pygame.draw.line(WIN.screen, colour, (x1, y1), (x2, y1)) #1 horizontal
    pygame.draw.line(WIN.screen, colour, (x1, y2), (x2, y2)) #2 horizontal
def main():
    global WIN
    WIN = Window()
    WIN.tiles = create_tiles()
    run = True
    while run:
        WIN.step()

if __name__ == "__main__":
    main()


