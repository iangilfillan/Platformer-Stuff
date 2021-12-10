import time
import pygame
import random
import sys
import os
pygame.init()
class Window:
    run = True
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    clock = pygame.time.Clock()
    fps = 45
    tilesize = 1
    background_colour = (0, 0, 0)
    background_colour = (255, 255, 255)
    fonts = {}
    count = 0
    def draw_window(self):
        if self.count > 0:
            pygame.display.update()
            return
        self.count += 1
        screen = self.screen
        screen.fill((255,255,255))
        drawing_rect = pygame.Rect(0, 0, self.tilesize, self.tilesize)
        max_colour = max(WIN.height // WIN.tilesize, WIN.width // WIN.tilesize)
        print(WIN.height // WIN.tilesize, WIN.width // WIN.tilesize)
        print(WIN.height // WIN.tilesize * WIN.width // WIN.tilesize)
        coefficient = (255 - 12) / max_colour
        for row_index in range(WIN.height // WIN.tilesize):
            for collumn_index in range(WIN.width // WIN.tilesize):
                drawing_rect.x = collumn_index*self.tilesize
                drawing_rect.y = row_index*self.tilesize
                colour = (12, round(coefficient * row_index) + 12, round(coefficient * collumn_index) + 12)
                pygame.draw.rect(screen, colour, drawing_rect)

        pygame.display.update()
    def step(self):
        self.clock.tick(self.fps)
        self.get_events()
        self.draw_window()
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
def main():
    global WIN
    WIN = Window()
    run = True
    while run:
        WIN.step()

if __name__ == "__main__":
    main()


