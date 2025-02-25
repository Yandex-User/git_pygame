import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 600, 512
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy bird')
pygame.display.set_icon(pygame.image.load('images/blueskin.png'))

font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 70)

img_bg = pygame.image.load('images/background-day.png')
img_bird = pygame.image.load('images/bluebird-midflap.png')
img_PT = pygame.image.load('images/m_pipe-green.png')
img_PB = pygame.image.load('images/pipe-green.png')

pygame.mixer.music.load('music/sound.mp3')
pygame.mixer.music.set_volume(0.12)
pygame.mixer.music.play(-1)

sound_fall = pygame.mixer.Sound('music/hit.wav')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 50, 50)

state = 'start'
timer = 10  # ждем 10 тиков во избежании непредвиденных ситуаций

pipes = []
pipes_scores = []
bgs = [pygame.Rect(0, 0, 288, 512)]

lives = 5
scores = 0

speed = 3
size = 200
gate = HEIGHT // 2

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

    speed = 3 + scores // 1000

    for x in range(len(bgs) - 1, -1, -1):
        bg = bgs[x]
        bg.x -= speed // 2

        if bg.right < -1:
            bgs.remove(bg)

        if bgs[len(bgs) - 1].right <= WIDTH:
            bgs.append(pygame.Rect(bgs[len(bgs) - 1].right,0,  200, 512))

    for i in range(len(pipes) - 1, -1, -1):  # иду с конца, так так при удалении труб было некое дерганье экрана
        elem = pipes[i]
        elem.x -= speed

        if elem.right < -1:  # при долгой игре забивается память и начинает лагать
            pipes.remove(elem)
            if elem in pipes_scores:
                pipes_scores.remove(elem)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
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

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, size - gate // 2))
            pipes.append(pygame.Rect(WIDTH, size + gate // 2, 52, HEIGHT - size + gate // 2))

            size += randint(-50, 50)

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for elem in pipes:
            if player.colliderect(elem):
                state = 'fall'
            if elem.right < player.left and elem not in pipes_scores:
                pipes_scores.append(elem)
                scores += 50
    elif state == 'fall':
        sound_fall.play()
        sy, ay = 0, 0
        gate = HEIGHT // 2

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60  # задержка 1 секунда
        else:
            state = 'end'
            timer = 120
    else:
        if timer == 0:
            play = False
    if click:
        ay = -2
    else:
        ay = 0

    window.fill(pygame.Color('black'))
    for bg in bgs:
        window.blit(img_bg, bg)
    for elem in pipes:
        if elem.y == 0:
            rect = img_PT.get_rect(bottomleft=elem.bottomleft)
            window.blit(img_PT, rect)
        else:
            rect = img_PB.get_rect(topleft=elem.topleft)
            window.blit(img_PB, rect)

    image = img_bird.subsurface(0, 0, 34, 24)
    image = pygame.transform.rotate(image, -sy * 1.9)  # задирает нос
    window.blit(image, player)

    text = font1.render("Счёт: " + str(scores), 1, pygame.Color('white'))
    window.blit(text, (10, 10))

    text = font1.render("Количество жизней: " + str(lives), 1, pygame.Color('white'))
    window.blit(text, (10, HEIGHT - 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()