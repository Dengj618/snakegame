
import pygame, sys, random
from pygame.locals import *

pygame.init()
size = width, height = 800, 700
screen = pygame.display.set_mode(size)
cell_size = 20
pygame.display.set_caption('SnakeGame-贪吃蛇')
bg = pygame.image.load("./images/01.png")
clock = pygame.time.Clock()  #

# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# 颜色定义
PINK = pygame.Color(250, 134, 126)  # 背景
BLACK = pygame.Color(0, 0, 0)  # 蛇身
RED = pygame.Color(255, 0, 0)  # 食物
blue = (0, 0, 255)
dark_blue = (0, 0, 139)
dark_gray = (40, 40, 40)


# 绘制贪吃蛇
def drawSnake(snake_Body):
    for i in snake_Body:
        pygame.draw.rect(screen, blue, pygame.Rect(i[0], i[1], 20, 20))


# 绘制食物
def drawFood(screen, food_Position):
    a = food_Position[0] * cell_size
    b = food_Position[1] * cell_size
    pygame.draw.rect(screen, RED, pygame.Rect(a, b, 20, 20))


# 绘制网格
def draw_grid(screen):
    for x in range(0, width, cell_size):  # draw 水平 lines
        pygame.draw.line(screen, dark_gray, (x, 0), (x, height))
    for y in range(0, height, cell_size):  # draw 垂直 lines
        pygame.draw.line(screen, dark_gray, (0, y), (width, y))


# 绘制成绩
def draw_score(screen, score):
    # pygame.font.get_fonts()
    # print(pygame.font.get_fonts())
    font = pygame.font.SysFont('arial', 30)
    scoreSurf = font.render('score: %s' % score, True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (width - 120, 10)
    screen.blit(scoreSurf, scoreRect)


# 蛇移动
def move_snake(direction, snake_Body, food_flag):
    (a, b) = snake_Body[0]
    n = len(snake_Body)
    if direction == UP:
        snake_Body.insert(0, (a, b - 20))
        if food_flag == 1:
            snake_Body.pop(n)
    if direction == DOWN:
        snake_Body.insert(0, (a, b + 20))
        if food_flag == 1:
            snake_Body.pop(n)
    if direction == LEFT:
        snake_Body.insert(0, (a - 20, b))
        if food_flag == 1:
            snake_Body.pop(n)
    if direction == RIGHT:
        snake_Body.insert(0, (a + 20, b))
        if food_flag == 1:
            snake_Body.pop(n)


# 结束
def terminate():
    pygame.quit()
    sys.exit()


# 判断蛇是否吃到食物
def snake_is_eat_food(snake_Body, food_Position,score):  # 如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
    (a, b) = snake_Body[0]
    x = food_Position[0] * 20
    y = food_Position[1] * 20
    flag = 1
    if a == x and b == y:
        food_Position = [random.randint(1, 30), random.randint(1, 30)]
        flag = 0
        score=score+1
    return food_Position, flag,score


# 判断蛇是否死亡
def snake_is_alive(snake_Body):
    tag = True
    (x, y) = snake_Body[0]
    if x > width or y > height or x < 0 or y < 0:
        tag = False

    for a, b in snake_Body[1:]:
        if (x, y) == (a, b):
            tag = False
    return tag


# 游戏结束信息显示
def show_gameover_info(screen):
    font = pygame.font.SysFont("arial",40)
    tip = font.render('press Q or ESC exit , press any restart the game~', True, (65, 105, 225))
    gameover = pygame.image.load('./images/GAMEOVER.png')
    screen.blit(gameover, (60, 0))
    screen.blit(tip, (80, 300))
    pygame.display.update()

    while True:  # 键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                    terminate()  # 终止程序
                else:
                    return  # 结束此函数, 重新开始游戏
def restart():
    x = random.randint(3, 30) * 20  # 随机位置
    y = random.randint(3, 30) * 20
    snake_Body = [(x, y), (x + 1 * cell_size, y), (x + 2 * cell_size, y)]  # 初始贪吃蛇
    drawSnake(snake_Body)
    print("重新开始")
    return snake_Body

def running_game(screen, clock):
    x = random.randint(3, 30) * 20  # 随机位置
    y = random.randint(3, 30) * 20
    snake_Body = [(x, y), (x + 1 * cell_size, y), (x + 2 * cell_size, y)]  # 初始贪吃蛇
    direction = LEFT
    drawSnake(snake_Body)  # 画出贪吃蛇
    food_Position = [random.randint(1, 30), random.randint(1, 30)]  # 给定第一枚食物的位置
    drawFood(screen, food_Position)  # 画出食物的位置
    pygame.display.update()  # update更新屏幕显示
    score = 0
    food_flag = 1  # 食物标记：0代表食物已被吃掉；1代表未被吃掉。
    while True:
        food_Position, food_flag ,score = snake_is_eat_food(snake_Body, food_Position,score)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        tag = snake_is_alive(snake_Body)
        if tag == False:
            show_gameover_info(screen)
            snake_Body=restart()
        move_snake(direction, snake_Body, food_flag)  # 移动蛇
        clock.tick(4)
        pygame.draw.rect(screen, PINK, (0, 0, width, height))
        screen.blit(bg, (140, 50))
        draw_score(screen, score)
        draw_grid(screen)
        drawFood(screen, food_Position)
        drawSnake(snake_Body)
        pygame.display.update()


running_game(screen, clock)
