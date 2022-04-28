import pygame
import math
import numpy as np

def r_math(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2+(y2 - y1) ** 2)


def getCoordsWithMatrix():

    A = np.matrix([[-2 * x0, -2 * y0, 1],
                   [-2 * x1, -2 * y1, 1],
                   [-2 * x2, -2 * y2, 1]])

    B = np.linalg.inv(A)

    dist = np.array([r_math(x0, y0, robot_rect[0] + 25, robot_rect[1] + 30),
                     r_math(x1, y1, robot_rect[0] + 25, robot_rect[1] + 30),
                     r_math(x2, y2, robot_rect[0] + 25, robot_rect[1] + 30)])

    y = np.matrix([[(dist[0] ** 2) - (x0 ** 2) - (y0 ** 2)],
                   [(dist[1] ** 2) - (x1 ** 2) - (y1 ** 2)],
                   [(dist[2] ** 2) - (x2 ** 2) - (y2 ** 2)]])

    res = B.dot(y)
    result = np.squeeze(np.asarray(res))

    return result[0], result[1]

pygame.init()

#-------------------Values--------------------------
W, H = 900, 600 #-> само поле W - tag_param*4, H - tag_param*3 -> 800, 525
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
tag_param = 25
x0, y0 = tag_param, 55
x1, y1 = tag_param, H - tag_param*3
x2, y2 = W - tag_param, H // 2
speed = 20
check_q = 0
check_w = 0
text = pygame.font.SysFont(None, 30)
text_r = pygame.font.SysFont(None, 28)
text_r12 = pygame.font.SysFont(None, 28)
text_r1 = text_r.render('r1', 1, BLACK, WHITE)
text_r2 = text_r12.render('r2', 1, BLACK, WHITE)
text_r3 = text_r.render('r3', 1, BLACK, WHITE)
#---------------------------------------------------

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Tags_system')
FPS = 60
clock = pygame.time.Clock()

#-----------------------------Image--------------------
pole_image = pygame.transform.scale(pygame.image.load('Pole.png'), (W - tag_param*4, H - tag_param*3))
#------------------------------------------------------


#--------------------------ROBOT--------------------
robot = pygame.Surface((52, 52))
robot_rect = robot.get_rect(center=(250, 250))
robot.fill(WHITE)
pygame.draw.aaline(robot, BLACK, (0, 50), (25, 0))
pygame.draw.aaline(robot, BLACK, (25, 0), (50, 50))
pygame.draw.aaline(robot, BLACK, (50, 50), (0, 50))
#---------------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if check_q == 0:
                    check_q = 1
                else:
                    check_q = 0
            if event.key == pygame.K_w:
                if check_w == 0:
                    check_w = 1
                else:
                    check_w = 0

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_LEFT]:
        robot_rect.x -= speed
    if key_pressed[pygame.K_RIGHT]:
        robot_rect.x += speed
    if key_pressed[pygame.K_UP]:
        robot_rect.y -= speed
    if key_pressed[pygame.K_DOWN]:
        robot_rect.y += speed

    if robot_rect.top <= tag_param + 5:
        robot_rect.top = tag_param + 5
    if robot_rect.bottom >= H - tag_param*2 - 5:
        robot_rect.bottom = H - tag_param*2 - 5
    if robot_rect.left <= tag_param*2 + 7:
        robot_rect.left = tag_param*2 + 7
    if robot_rect.right >= W - tag_param*2 - 7:
        robot_rect.right = W - tag_param*2 - 7

    sc.fill(WHITE)

    if check_w:
        sc.blit(pole_image, (tag_param*2, tag_param))
    else:
        pygame.draw.rect(sc, BLACK, (tag_param*2, tag_param, W - tag_param*4, H - tag_param*3), 2) #(surface, (red, green, blue), (x, y, width, height), 2)

    sc.blit(robot, robot_rect)

    if check_q:
        pygame.draw.circle(sc, BLACK, (x0, y0), int(r_math(x0, y0, robot_rect[0]+25, robot_rect[1]+30)), 1)
        pygame.draw.circle(sc, BLACK, (x1, y1), int(r_math(x1, y1, robot_rect[0]+25, robot_rect[1]+30)), 1)
        pygame.draw.circle(sc, BLACK, (x2, y2), int(r_math(x2, y2, robot_rect[0]+25, robot_rect[1]+30)), 1)

    pygame.draw.circle(sc, BLACK, (x0, y0), tag_param, 2)
    pygame.draw.circle(sc, BLACK, (x1, y1), tag_param, 2)
    pygame.draw.circle(sc, BLACK, (x2, y2), tag_param, 2)

    pygame.draw.aaline(sc, BLACK, (x0, y0), (robot_rect[0]+25, robot_rect[1]+30))
    pos_r1 = text_r1.get_rect(center=((robot_rect[0]+25 + x0) // 2,
                                      (robot_rect[1]+30 + y0) // 2))
    sc.blit(text_r1, pos_r1)

    pygame.draw.aaline(sc, BLACK, (x1, y1), (robot_rect[0]+25, robot_rect[1]+30))
    pos_r2 = text_r2.get_rect(center=((robot_rect[0] + 25 + x1) // 2,
                                      (robot_rect[1] + 30 + y1) // 2))
    sc.blit(text_r2, pos_r2)

    pygame.draw.aaline(sc, BLACK, (x2, y2), (robot_rect[0]+25, robot_rect[1]+30))
    pos_r3 = text_r3.get_rect(center=((robot_rect[0] + 25 + x2) // 2,
                                      (robot_rect[1] + 30 + y2) // 2))
    sc.blit(text_r3, pos_r3)
    x_robot, y_robot = getCoordsWithMatrix()
    sc_text = text.render(f'r1 = {r_math(x0, y0, robot_rect[0]+25, robot_rect[1]+30):.0f},'
                          f' r2 = {r_math(x1, y1, robot_rect[0]+25, robot_rect[1]+30):.0f},'
                          f' r3 = {r_math(x2, y2, robot_rect[0]+25, robot_rect[1]+30):.0f},'
                          f' x_robot = {x_robot - tag_param*2:.0f},'
                          f' y_robot = {y_robot - tag_param:.0f}',
                          1, BLACK, WHITE)
    pos = sc_text.get_rect(center=(W // 2, H - tag_param*2 + 15))
    sc.blit(sc_text, pos)
    pygame.display.update()

    clock.tick(FPS)
