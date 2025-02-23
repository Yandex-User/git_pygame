import pygame
pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 50, 50)

state = 'start'
timer = 60

pipes = []

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    for elem in pipes:
        elem.x -= 2

    if state == 'start':
        if click and timer == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.02
        player.y = py
    elif state == 'play':
        if click:
            ay = -3
        else:
            ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.95  # для более плавной картинки
        player.y = py

        if len(pipes) == 0:
            pipes.append(pygame.Rect(WIDTH - 100, 0, 50, 200))
            pipes.append(pygame.Rect(WIDTH - 100, 400, 50, 200))

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'
    elif state == 'fall':
        sy, ay = 0, 0
        state = 'start'
        timer = 120 # задержка 2 секунды
    else:
        pass
    if click:
        ay = -3
    else:
        ay = 0


    window.fill(pygame.Color('black'))
    for elem in pipes:
        pygame.draw.rect(window, pygame.Color('green'), elem)

    pygame.draw.rect(window, pygame.Color('orange'), player)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()