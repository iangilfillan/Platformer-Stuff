import time
import pygame
import random
import sys
import os
import re
from collections import OrderedDict
import pathfinding_mod as pathfinding
import gen_mountain_rects as mountain
pygame.init()
class Window:
    run = True
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    clock = pygame.time.Clock()
    fps = 60
    tilesize = 48
    grav = 5
    terminal_velocity = 16
    water_terminal_velocity = 1
    camera_offset = (0, 0)
    background_colour = (0, 0, 0)
    last_grounded = 0
    background_colour = (135, 206, 235) #sly blue
    drawing_rect = pygame.Rect(0, 0, tilesize, tilesize)
    tile_rect = pygame.Rect(0, 0, tilesize, tilesize)
    m_rects1 = mountain.generate(width * 2, height, tilesize // 2, pull_down = 0.3)
    m_rects2 = mountain.generate(width * 2, height, tilesize // 2, pull_down = 0.6)
    c_rects1 = []
    m_offset = -width // 2
    fonts = {}
    types = OrderedDict(air = (255, 255, 255),
                        grass = (126, 200, 80),
                        water = (156, 211, 219),
                        rock = (155, 163, 164))
    cloud_timer = time.time()
    def draw_window(self):
        tiles = self.tiles
        screen = self.screen
        tilesize = self.tilesize
        camera_x, camera_y = self.camera_offset
        drawing_rect_x = 0
        screen.fill(self.background_colour)

        sx, sy = PLAYER.starting_pos
        max_offset = [
            len(tiles) * self.tilesize - 203,
            len(tiles[0]) * self.tilesize + sy
        ]
        if max_offset[0] <= -camera_x:
            drawing_rect_x = -camera_x - max_offset[0]
            camera_x = -max_offset[0]
        elif 0 >= -camera_x:
            drawing_rect_x = -camera_x
            camera_x = 0
        
        m1_offset = camera_x // 10 + self.m_offset, camera_y // 10
        m2_offset = camera_x // 7 + self.m_offset, camera_y // 7
        r_size = tilesize // 2
        self.drawing_rect.w = r_size
        for rect in self.m_rects1:
            x, y = rect
            if x + m1_offset[0] > self.width or x + m1_offset[0] < -tilesize / 2:
                 continue
            self.drawing_rect.x, self.drawing_rect.y = x + m1_offset[0], y + m1_offset[1]
            self.drawing_rect.h = self.height
            pygame.draw.rect(screen, (128, 128, 144), self.drawing_rect)
        
        for rect in self.m_rects2:
            x, y = rect
            if x + m2_offset[0] > self.width or x + m2_offset[0] < -tilesize / 2:
                 continue
            self.drawing_rect.x, self.drawing_rect.y = x + m2_offset[0], y + m2_offset[1]
            self.drawing_rect.h = self.height
            pygame.draw.rect(screen, (144, 144, 144), self.drawing_rect)

        self.drawing_rect.w, self.drawing_rect.h = tilesize // 2, tilesize // 2
        for cloud in self.c_rects1:
            for rect in cloud:
                x, y = rect
                self.drawing_rect.x = x
                self.drawing_rect.y = y
                pygame.draw.rect(self.screen, (255, 255, 255), self.drawing_rect)
                print(x, y)
        count = 0
        #drawing tiles
        self.drawing_rect.w, self.drawing_rect.h = tilesize, tilesize
        for row_index, row in enumerate(tiles):
            for collumn_index, colour_index in enumerate(row):
                if colour_index == 0:
                    continue
                colour = list(self.types.values())[colour_index]
                self.drawing_rect.x = collumn_index*self.tilesize + camera_x
                self.drawing_rect.y = row_index*self.tilesize + camera_y
                pygame.draw.rect(screen, colour, self.drawing_rect)
                count += 1

        #drawing creatures
        for c in CREATURES:
            c.drawing_rect.x = c.x + camera_x
            c.drawing_rect.y = c.y + camera_y
            pygame.draw.rect(screen, c.colour, c.drawing_rect)
        #drawing character
        text, wh = self.get_text(f"{round(PLAYER.x)} {round(PLAYER.y)}", fontsize = 32)
        self.screen.blit(text, (0, 0))
        text, _ = self.get_text(f"{round(PLAYER.vel[0])}, {round(PLAYER.vel[1], 1)}", fontsize = 32)
        self.screen.blit(text, (wh[0]* 2, 0))
        PLAYER.drawing_rect.x += drawing_rect_x
        pygame.draw.rect(self.screen, PLAYER.colour, PLAYER.drawing_rect)
        PLAYER.drawing_rect.x -= drawing_rect_x
        #update the display
        pygame.display.update()
    def step(self):
        self.clock.tick(self.fps)
        self.draw_window()
        self.get_events()
        if not self.run:
            pygame.quit()
            sys.exit()
        if time.time() > self.cloud_timer:
            self.c_rects1.append(cloud_gen())
            if len(self.c_rects1) > 2:
                del self.c_rects1[0]
            self.cloud_timer = time.time() + random.randint(1, 10)
        for cloud in self.c_rects1:
            for rect in cloud:
                rect[0] += 2
        vx, vy = PLAYER.vel
        #if not self.is_grounded(PLAYER.rect):
        m = 1
        terminal_velocity = self.terminal_velocity
        if self.is_grounded(PLAYER.rect, PLAYER):
            PLAYER.jump_num = 1
        if self.is_submerged(PLAYER.rect):
            m /= 2
            terminal_velocity = self.water_terminal_velocity
        if vy + self.grav / self.fps * m <= terminal_velocity:
            PLAYER.vel = vx, vy + self.grav / self.fps * m
        vx, vy = PLAYER.vel
        PLAYER.move(x = vx)
        PLAYER.move(y = vy)
        for c in CREATURES:
            c.pathfind()
                
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                self.keypress_inputs(event.key)
        self.keyheld_inputs()
    def get_text(self, text, font = "arial", fontsize = 16, colour = (0, 0, 0)):
        """returns rendered text and a tuple of (text_width, text_height) assigns it to main class as a memo"""
        if "fonts" not in locals():
            self.fonts = {}
        if (font, fontsize) not in self.fonts:
            self.fonts[(font, fontsize)] = pygame.font.SysFont(font, fontsize)
        font = self.fonts[(font, fontsize)]

        return font.render(text, 1, colour), font.size(text)
    def keypress_inputs(self, key):
        if key == pygame.K_l:
            self.tiles = load_map()
        elif key == pygame.K_SPACE or key == pygame.K_w:
            PLAYER.rect.x, PLAYER.rect.y = PLAYER.x, PLAYER.y
            if self.is_submerged(PLAYER.rect) or self.is_grounded(PLAYER.rect, PLAYER) or PLAYER.jump_num > 0:
                PLAYER.jump(PLAYER.jump_height)
                PLAYER.jump_num -= 1
    def keyheld_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            PLAYER.move(x = -1)
        if keys[pygame.K_a]:
            PLAYER.move(x = 1)
    def is_colliding_with_tile(self, rect):
        tiles = self.tiles
        for i in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            x = rect.x / self.tilesize
            y = rect.y / self.tilesize
            a, b = i
            x += a * rect.w / self.tilesize
            y += b * rect.h / self.tilesize
            x, y = int(x), int(y)
            
            if y >= 0 and y < len(tiles):
                if x >= 0 and x < len(tiles[y]):
                    tile = tiles[y][x]
                    if tile != 0 and tile != 2:
                        return y, x
        return False
    def is_grounded(self, rect, cl_ob):
        rect.y += 2
        if self.is_colliding_with_tile(rect):
            cl_ob.last_grounded = time.time()
        rect.y -= 2
        if time.time() - cl_ob.last_grounded <= 0.1:
            return True
        return False
    def inside_tile(self, rect, tile):
        sx = int(rect.x / self.tilesize)
        sy = int(rect.y / self.tilesize)
        if tile != (sy, sx):
            return False
        for i in [(0, 1), (1, 0), (1, 1)]:
            x, y = i
            sx = int((rect.x / self.tilesize) + x * self.w)
            sy = int((rect.y / self.tilesize) + y * self.h)
            if tile != (sy, sx):
                return False
        return True
    def dir_to_center(self, rect):
        tilesize = self.tilesize
        sx = int((rect.x + self.width / 2)/ tilesize)
        sy = int((rect.y + self.height / 2)/ tilesize)
        dx, dy = sx * tilesize - self.x, sy * tilesize - self.y
        if dx != 0:
            dx = dx / abs(dx)
        if dy != 0:
            dy = dy / abs(dy)
        return dx, dy
    def is_submerged(self, rect):
        tilesize = self.tilesize
        tiles = self.tiles
        x, y = int((rect.x + rect.w / 2) / tilesize), int((rect.y + rect.h) / tilesize)
        if y > -1 and y < len(tiles):
            if x > -1 and x < len(tiles[y]):
                if tiles[y][x] == 2:
                    return True
        return False


class Character:
    width, height = 24, 36
    w, h = width, height
    image = None
    colour = 212, 175, 55
    move_speed = 5
    swim_speed = 2.5
    jump_num = 2
    vel = (0, 0)
    jump_height = 2.5
    last_grounded = time.time()
    def __init__(self, x, y):
        #self.starting_pos = (WIN.width / 2 - self.width / 2, WIN.height / 1.2)
        self.starting_pos = x + self.w + WIN.tilesize/2, y + WIN.tilesize/2 - self.h
        self.rect = pygame.Rect(self.starting_pos, (self.w, self.h))
        self.x, self.y = self.starting_pos
        self.starting_pos = (WIN.width / 2 - self.width / 2, WIN.height / 2 - self.height / 2)
        self.drawing_rect = pygame.Rect(self.starting_pos, (self.w, self.h))
    def move(self, x = 0, y = 0):
        og_x, og_y = x, y
        s = self.move_speed
        sw = s
        if WIN.is_submerged(self.rect):
            sw = self.swim_speed
        self.x -= x * sw
        self.y += y * s
        self.rect.x, self.rect.y = self.x, self.y
        if WIN.is_colliding_with_tile(self.rect) != False:
            vx, vy = self.vel
            if og_x != 0: # if it's x to move
                self.x += og_x * sw
                vx = 0
            if og_y != 0: # if it's y to move
                self.y -= og_y * s
                vy = 0
            self.vel = vx, vy
            self.rect.x, self.rect.y = self.x, self.y
            return
        starting_x, starting_y = PLAYER.starting_pos
        WIN.camera_offset = -int(self.x - starting_x), -int(self.y - starting_y)
    def jump(self, vel):
        vx, vy = self.vel
        if WIN.is_submerged(self.rect):
            vel /= 1.5
        self.vel = vx, -vel * 60 / WIN.fps
class Creature:
    width, height = 36, 24
    w, h = width, height
    move_speed = 2
    vel = (0, 0)
    next = (0, 0)
    colour = (128, 128, 128)
    last_grounded = time.time()
    prev_time = time.time()
    def __init__(self, spawn_pos):
        x, y = spawn_pos
        spawn_pos = x + self.w + WIN.tilesize/2, y + WIN.tilesize/2 - self.h
        self.default_pos = spawn_pos
        self.x, self.y = spawn_pos
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.drawing_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def move(self, x = 0, y = 0):
        og_x, og_y = x, y
        s = self.move_speed
        self.x -= x * s
        self.y -= y * s
        self.rect.x, self.rect.y = self.x, self.y
        if WIN.is_colliding_with_tile(self.rect) != False:
            vx, vy = self.vel
            if og_x != 0:
                self.x += og_x * s
                vx = 0
            if og_y != 0:
                self.y -= og_y * s
                vy = 0
            self.vel = vx, vy
            return
    def jump(self, vel):
        vx, vy = self.vel
        self.vel = vx, vy-vel * 60 / WIN.fps
    def pathfind(self):
        sx = int(self.x / WIN.tilesize)
        sy = int(self.y / WIN.tilesize)
        if self.next != (0, 0):
            if self.next == (sy, sx):
                self.rect.x = self.x
                self.rect.y = self.y
                if not WIN.inside_tile(self.rect, self.next):
                    d = WIN.dir_to_center(self.rect)
                    self.move(x = d[1], y = d[0])
                    return

        px = int(PLAYER.x / WIN.tilesize)
        py = int(PLAYER.y / WIN.tilesize)
        path = pathfinding.pathfind(WIN.tiles, start = (sy, sx), end = (py, px))
        if path == None:
            return
        if len(path) == 1:
            Next = path[0]
        else:
            Next = path[1]
        y, x = Next
        #self.y, self.x = y, x
        self.move(y = sy - y, x = sx - x)
        self.next = sy - y, sx - x
        #print(vy, vx)

def cloud_gen():
    s = []
    with open("cloud_types.txt", "r") as File:
        s = File.read()
        s = s.split("\n")
    s = random.choice(s)
    c_rects = []
    if True:
        matches = re.findall(r"\d+, \d+", s)
        for l in matches:
            tup = []
            for c in l:
                if c.isnumeric():
                    tup.append(int(c))
            x, y = tup
            y += random.randint(1, 10)
            c_rects.append([x * WIN.tilesize//2, y * WIN.tilesize//2])
    return c_rects
                

def load_map():
    global PLAYER
    global CREATURES
    tiles = []
    CREATURES = []
    with open("current_save.txt", "r") as File:
        lines = File.readlines()
    
    for line in lines:
        tiles.append([])
        matches = re.findall(r"\d|[ps]", line)
        for match in matches:
            if not match.isalpha():
                tiles[-1].append(int(match))
            else:
                y, x = (len(tiles) - 1) * WIN.tilesize, (len(tiles[-1])-1) * WIN.tilesize
                if match == "p":
                    PLAYER = Character(x, y)
                elif match == "s":
                    c = Creature((x, y))
                    CREATURES.append(c)
                tiles[-1].append(0)
    return tiles
def create_tiles():
    tiles = load_map()
    return tiles

def main():
    global WIN
    #global PLAYER
    WIN = Window()
    #PLAYER = Character()
    WIN.tiles = create_tiles()
    run = True
    while run:
        WIN.step()

if __name__ == "__main__":
    main()


