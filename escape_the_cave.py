import pygame
import random
import time


class Window:
    def __init__(self, win_width, win_height, win_caption):
        self.win_width = win_width
        self.win_height = win_height
        self.win_caption = win_caption
        self.window = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption(self.win_caption)

    def fill(self):
        self.window.fill((0, 0, 0))


class Player:
    def __init__(self, colour_r, colour_g, colour_b, left_walk, right_walk, left_jump, right_jump, idle):
        self.colour_r = colour_r
        self.colour_g = colour_g
        self.colour_b = colour_b
        self.left = False
        self.right = False
        self.walk_count = 0
        self.left_walk = left_walk
        self.right_walk = right_walk
        self.left_jump = left_jump
        self.right_jump = right_jump
        self.idle = idle

    def draw(self, win_, x_rect, y_rect, char_jump):
        if self.walk_count + 1 >= 18:
            self.walk_count = 0
        if self.left is True and char_jump is False:
            win_.blit(self.left_walk[self.walk_count // 3], (x_rect, y_rect))
            self.walk_count += 1
        elif self.right is True and char_jump is False:
            win_.blit(self.right_walk[self.walk_count // 3], (x_rect, y_rect))
            self.walk_count += 1
        elif self.left is True and char_jump is True:
            win_.blit(self.left_jump, (x_rect, y_rect))
            self.walk_count += 1
        elif self.right is True and char_jump is True:
            win_.blit(self.right_jump, (x_rect, y_rect))
            self.walk_count += 1
        else:
            win_.blit(self.idle, (x_rect, y_rect))


class Platform:
    def __init__(self, colour_r, colour_g, colour_b, x_plat, y_plat, w_plat, h_plat):
        self.colour_r = colour_r
        self.colour_g = colour_g
        self.colour_b = colour_b
        self.x_plat = x_plat
        self.y_plat = y_plat
        self.w_plat = w_plat
        self.h_plat = h_plat

    def draw(self, win_plat):
        pygame.draw.rect(win_plat, (self.colour_r, self.colour_g, self.colour_b),
                         (self.x_plat, self.y_plat, self.w_plat, self.h_plat))


def create_platforms(no_of_platforms, window_height):
    platforms = []
    step_plat = round((window_height - 100) / no_of_platforms)
    poss_heights = []
    for poss in range(0, no_of_platforms):
        poss_heights.append(step_plat * poss)
    heights = poss_heights
    print(heights)
    for platform in range(no_of_platforms):
        if len(heights) > 1:
            height_plat = heights[random.randint(0, len(heights)-1)]
            heights.remove(height_plat)
        else:
            height_plat = heights[0]
        platforms.append(Platform(0, 255, 0, random.randint(100, win.win_width-100),
                                  height_plat, random.randint(50, 100), 10))
    return platforms


walkRight = [pygame.image.load('adventurer-run-00-1.3.png'),
             pygame.image.load('adventurer-run-01-1.3.png'),
             pygame.image.load('adventurer-run-02-1.3.png'),
             pygame.image.load('adventurer-run-03-1.3.png'),
             pygame.image.load('adventurer-run-04-1.3.png'),
             pygame.image.load('adventurer-run-05-1.3.png')]
walkLeft = [pygame.image.load('adventurer-run-00-1.3 - Left.png'),
            pygame.image.load('adventurer-run-01-1.3 - Left.png'),
            pygame.image.load('adventurer-run-02-1.3 - Left.png'),
            pygame.image.load('adventurer-run-03-1.3 - Left.png'),
            pygame.image.load('adventurer-run-04-1.3 - Left.png'),
            pygame.image.load('adventurer-run-05-1.3 - Left.png')]
char = pygame.image.load('adventurer-idle-03-1.3.png')
jump = [pygame.image.load('adventurer-smrslt-00-1.3.png'),
        pygame.image.load('adventurer-smrslt-00-1.3 - Left.png')]
bg = pygame.image.load('bg.png')


pygame.init()
x = 250
y = 400
width = 50
height = 37
velocity = 15
jump_count = 10
run = True
is_jump = False
is_crouch = False
crouch_count = 0
rect_y = y
y_plats = [500, 400, 300, 200, 100]
is_land = True
down = False
on_platform = False
clock = pygame.time.Clock()

win = Window(1000, 500, "Escape The Cave!")
player = Player(255, 0, 0, left_walk=walkLeft, right_walk=walkRight, left_jump=jump[1], right_jump=jump[0], idle=char)
main_platform = Platform(255, 0, 0, 0, rect_y + height, win.win_width, 10)
rand_plats = create_platforms(12, 500)
jumped = False
y_s = []
difficulty = 2
count = 500
c = 1
while run:
    clock.tick(27)
    y_s.append(y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    y_in_game = y
    height_in_game = height
    keys = pygame.key.get_pressed()
    if not is_jump:
        is_land = True
        y_in_game = y
        if keys[pygame.K_LEFT]:
            x -= velocity
            player.left = True
            player.right = False
        elif keys[pygame.K_RIGHT]:
            x += velocity
            player.left = False
            player.right = True
        else:
            player.left = False
            player.right = False
        if keys[pygame.K_UP]:
            is_jump = True
            jumped = True
        if player.left is False and player.right is False:
            player.walk_count = 0
    elif is_jump is True:
        is_land = False
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= (jump_count ** 2) * 0.5 * neg
            y_in_game = y
            on_platform = False
            jump_count -= 1
        else:
            down = False
            is_jump = False
            jump_count = 10
        if keys[pygame.K_LEFT]:
            x -= velocity
            player.left = True
            player.right = False
        elif keys[pygame.K_RIGHT]:
            x += velocity
            player.left = False
            player.right = True
    if len(y_s) >= 2:
        if on_platform is False and jumped is True:
            if y_s[-1] > y_s[-2]:
                down = True
    for random_platform in range(0, len(rand_plats)):
        plat_x = rand_plats[random_platform].x_plat
        plat_y = rand_plats[random_platform].y_plat
        plat_width = rand_plats[random_platform].w_plat
        list_of_plat_x = list(range(plat_x, (plat_x + plat_width)))
        for xes in range(len(list_of_plat_x)):
            if x + width / 2 == list_of_plat_x[xes] and plat_y - 65 < y <= plat_y - 10:
                if down is True:
                    # print(f"Platform X: {rand_plats[random_platform].x_plat} | Platform Y: "
                    #       f"{rand_plats[random_platform].y_plat} | Character X, Y: {x}, {y}")
                    y = plat_y
                    jump_count = -11
                    down = False
                    is_jump = False
                    on_platform = True
                    plat_idx = random_platform
    if on_platform is True:
        y = rand_plats[plat_idx].y_plat - height
        list_of_plat_x = list(range(rand_plats[plat_idx].x_plat,
                                    rand_plats[plat_idx].x_plat + rand_plats[plat_idx].w_plat))
        if x + width / 2 not in list_of_plat_x:
            jump_count = 0
            is_jump = False
            down = True
            on_platform = False
    if on_platform is False and jumped is True:
        if is_jump is False:
            y -= (2 ** 2) * 0.5 * -8
    win.window.blit(bg, (0, 0))
    y_in_game = y
    player.draw(win_=win.window, x_rect=x, y_rect=y_in_game, char_jump=is_jump)
    if jumped is False:
        main_platform.draw(win_plat=win.window)
    if c % count == 0:
        difficulty += 1
    for plat in range(len(rand_plats)):
        if rand_plats[plat].y_plat < win.win_height:
            rand_plats[plat].y_plat += difficulty
        else:
            rand_plats[plat].y_plat = 0
            rand_plats[plat].x_plat = random.randint(100, win.win_width-100)
            rand_plats[plat].w_plat = random.randint(50, 100)
        rand_plats[plat].draw(win.window)
    pygame.display.update()
    if x <= 0 or x >= win.win_width:
        run = False
    if y >= win.win_height - height:
        run = False
    c += 1
    if difficulty > 5:
        run = False
        print("You win!")
    print(f"Difficulty: {difficulty - 1}")
pygame.quit()
