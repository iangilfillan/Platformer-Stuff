import pygame

pygame.init()
WIN = pygame.display.set_mode((900, 600))

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    WIN.fill((200, 200, 200))
    x, y = pygame.mouse.get_pos()
    pygame.draw.line(WIN, (128, 128, 128), (x + 48, y - 24), (x + 48, y + 24), width = 48)
    pygame.draw.line(WIN, (128, 128, 128), (x - 48, y - 24), (x - 48, y + 24), width = 48)
    pygame.draw.line(WIN, (128, 128, 128), (x - 24, y + 48), (x + 24, y + 48), width = 48)
    pygame.draw.line(WIN, (128, 128, 128), (x - 24, y - 48), (x + 24, y - 48), width = 48)
    pygame.display.update()