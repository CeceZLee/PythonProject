# -*- coding: utf-8 -*-
# @Time    : 2/25/21 12:09 上午
# @Author  : Boxuan
# @FileName: fly.py
# @Software: PyCharm


import pygame, random, math


# 1.初始化界面: screen大小，游戏窗口名称，图像icon, 背景icon
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('FlyGame')
icon = pygame.image.load('ufo.jpg')  #加载图像，然后显示icon.游戏的icon设置为一个ufo
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.png')

# 添加分数
score = 0
font_score = pygame.font.Font('freesansbold.ttf', 32)
def show_score():
    text = f'Score:{score}'
    score_render = font_score.render(text, True, (0,255,0)) #渲染字体，显示分数
    screen.blit(score_render,(10,10))

# 判断游戏是否结束
is_over = False
font_over = pygame.font.Font('freesansbold.ttf', 64)
def check_is_over():
    if is_over:
        text = 'Game Over'
        over_render = font_over.render(text, True, (255,0,0))
        screen.blit(over_render, (200,250))

# 5. player飞机
playImg = pygame.image.load('player.png')
playX = 380  #player的初始坐标。左上角的是（0，0）右下角的是（800，600）
playY = 500
playStep = 0 # 为了让飞机能够移动，设置一个变量作为移动的step

# 添加敌人, 将敌人写成一个class，用于添加多个敌人
number_of_enemies = 6
class Enemy():
    def __init__(self):
        self.Img = pygame.image.load('enemy.png')
        self.x = random.randint(200,600)
        self.y = random.randint(50,100)
        self.step = random.uniform(-4,4)
    #被射中时，恢复位置
    def reset(self):
        self.x = random.randint(200,600)
        self.y = random.randint(50,100)

# 定义一个数组用来储存所有生成的enemy.
# 如果在main loop中生成enemy会造成每一次的enemy是不同的（random），
# 但是use case需要每一帧的enemy都是相同的，所以需要一个data structure来储存
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())

# 把show enemy写成一个function
def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.Img, (e.x, e.y))
        e.x += e.step
        if e.x > 736 or e.x < 0:
            e.step *= -1
            e.y += 30
        if e.y >450:
            is_over = True  #如果只在函数里面改，会被当成局部变量。
            enemies.clear()

# 定义子弹类
class Bullet():
    def __init__(self):
        self.Img = pygame.image.load('bullet.png')
        self.x = playX + 16 #(64-32)/2
        self.y = playY-3
        self.step = 10

    def hit(self):
        global score  # change the value of a global variable inside a function: use `global` keyword
        for e in enemies:  #for loop,对于每一个敌人do sth
            if (distance(self.x, self.y, e.x, e.y)) < 50:
                e.reset()
                bullet.remove(self)
                score += 1

bullet = [] # 创建一个数组，保存现有的子弹（支持连发）。子弹发射出界之后需要从list中剔除

def show_bullet():
    for b in bullet:  # 写成for loop，才能在main loop中调用时，每一次把bullet中所有存在的子弹都build出来。
        screen.blit(b.Img, (b.x, b.y))
        b.hit()  # 在show bullet函数中添加判断射中的方法
        b.y -= 10
        if b.y < 0:
            bullet.pop(0)

# 检测子弹和敌人的距离
def distance(bx, by, ex, ey):
    x = bx-ex
    x *= x
    y = by-ey
    y *= y
    return math.sqrt(x+y)

# 2.游戏主循环：初始化之后只能显示一下就结束。
# 添加主循环，就相当于每一帧都做循环中的事情，游戏就可以运行了。
running = True #不把循环条件hardcode，而是写成一个单独的变量，从而以后可以更改变量的值，==》以更改循环条件。
while running:
    screen.blit(bgImg, (0,0))  #最底层画第一张图。background
    show_score()
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False  #一旦触发了退出事件，就将变量running的值改成false，结束循环。不然就是死循环。
        # 所有的键盘事件
        # 让飞机移动，通过识别键盘动作，更改移动的step值，每次迭代x坐标，将飞机画在新的位置。
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playStep = 5
            if event.key == pygame.K_LEFT:
                playStep = -5
            if event.key == pygame.K_SPACE:
                bullet.append(Bullet()) #键盘按下时创建一个子弹，添加到列表中，one line

        if event.type == pygame.KEYUP:
            playStep = 0

    # 防止player下标出界
    if playX >736:
        playX = 736
    if playX <0:
        playX = 0

    screen.blit(playImg,(playX, playY)) # 上层画飞机，注意画图的顺序，在每一次loop的是时候都是从前往后 = 从底层到上层，顺序不能破坏。不然就遮住了。
    playX += playStep

    show_enemy()
    show_bullet()
    check_is_over()

    pygame.display.update() #每一次画完，都要update一下，一个by default必须有的操作

