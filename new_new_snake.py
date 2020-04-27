#  let's have another pop at snake
import turtle
import random
import time
import numpy as np
import pickle
import math


class Window:
    def __init__(self, title, background_colour, window_width, window_height, episode, l_r):
        self.win = turtle.Screen()
        self.win.title(title)
        self.win.bgcolor(background_colour)
        self.win.setup(width=window_width, height=window_height)
        self.win.tracer(0)
        self.win.listen()
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 275)
        self.pen.write("Jeremy, the snake RL AI.", align="center", font=("Courier", 16, "normal"))
        self.pen.goto(-250, 275)
        self.pen.write(f"Episode: {episode}")
        self.pen.goto(-250, 220)
        self.pen.write(f"Learning rate: {l_r}")

    def update_window(self):
        self.win.update()


class Snake:
    def __init__(self, colour):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

    def move(self, action_int):
        move_val = 20
        if action_int == 0:
            x = self.head.xcor()
            self.head.setx(x + move_val)
        if action_int == 1:
            x = self.head.xcor()
            self.head.setx(x - move_val)
        if action_int == 2:
            y = self.head.ycor()
            self.head.sety(y + move_val)
        if action_int == 3:
            y = self.head.ycor()
            self.head.sety(y - move_val)

    def reset_loc(self):
        self.head.setx(0)
        self.head.sety(0)


class Snack:
    def __init__(self):
        self.snack = turtle.Turtle()
        self.snack.speed(0)
        self.snack.shape("circle")
        self.snack.color("green")
        self.snack.penup()
        self.snack.goto(0, 0)
        self.possible_locations = []
        for poss in range(-13, 13):
            self.possible_locations.append(poss)

    def set_loc(self):
        self.snack.sety((self.possible_locations[random.randint(0, (len(self.possible_locations) - 1))]) * 20)
        self.snack.setx((self.possible_locations[random.randint(0, (len(self.possible_locations) - 1))]) * 20)


def auto_choose_action(x_difference, y_difference):
    action_int = 0
    if x_difference > 0:
        action_int = 0
    if x_difference < 0:
        action_int = 1
    if y_difference > 0:
        action_int = 2
    if y_difference < 0:
        action_int = 3
    return action_int


# def create_possible_states():
#     poss_states = []
#     num = 1
#     for first in range(-32, 32):
#         for second in range(-32, 32):
#             for xcor in range(-21, 21):
#                 for ycor in range(-21, 21):
#                     for scor in range(0, 20):
#                         poss_states.append([first, second, xcor, ycor, scor])
#                         print(f"Iteration {num}: State: {poss_states[-1]}")
#                         num += 1
#     return poss_states

def create_possible_states():
    poss_states = []
    num = 1
    for first in range(-2, 2):
        for second in range(-2, 2):
            for obstaclex in range(-3, 3):
                for obstacley in range(-3, 3):
                    for scor in range(0, 20):
                        poss_states.append([first, second, obstaclex, obstacley, scor])
                        print(f"Iteration {num}: State: {poss_states[-1]}")
                        num += 1
    return poss_states


learning_rate = 0.1
# possible_states = create_possible_states()
# with open("/Users/timandersson1/Desktop/python files not dotpy/possible combinations snake.txt", "wb") as fp:
#     pickle.dump(possible_states, fp)
with open("/Users/timandersson1/Desktop/python files not dotpy/possible combinations snake.txt", "rb") as fap:
    list_possible_states = pickle.load(fap)
dim = len(list_possible_states)

# q_table = np.random.uniform(low=-2, high=0, size=(dim, 4))
q_table = np.loadtxt('q_table_snake.csv', delimiter=',')

episodes = 1000
print(len(list_possible_states))
print(q_table.shape)
actions_n = 4
epoch = 1000
scalar = 20
a = 0
discount = 0.9
#  tweak parameters
while a < episodes:
    win = Window("Snake", "black", 600, 600, a, learning_rate)
    snake = Snake("red")
    snack = Snack()
    snack.set_loc()
    x_co_ords = []
    y_co_ords = []
    snake_body = []
    x_diffs = []
    y_diffs = []
    distances = []
    scores = []
    over = False
    score = 0
    p = 0
    r_plus = 0
    obstacle_distance_x_right = 0
    obstacle_distance_x_left = 0
    obstacle_distance_y_up = 0
    obstacle_distance_y_down = 0
    obstacle_x = 0
    obstacle_y = 0
    while over is False:
        time.sleep(0.05)
        reward = -5
        obstacle_distance_x_right = 15 - (snake.head.xcor() / scalar)
        obstacle_distance_x_left = 15 + (snake.head.xcor() / scalar)
        obstacle_distance_y_up = 15 - (snake.head.ycor() / scalar)
        obstacle_distance_y_down = 15 + (snake.head.ycor() / scalar)
        x_co_ords.append(snake.head.xcor())
        y_co_ords.append(snake.head.ycor())
        x_diff = - 1 * ((snake.head.xcor() / scalar) - (snack.snack.xcor() / scalar))
        y_diff = - 1 * ((snake.head.ycor() / scalar) - (snack.snack.ycor() / scalar))
        scores.append(score)
        if x_diff > 0:
            x_dir = 1
        elif x_diff < 0:
            x_dir = -1
        else:
            x_dir = 0
        if y_diff > 0:
            y_dir = 1
        elif y_diff < 0:
            y_dir = -1
        else:
            y_dir = 0
        current_distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        if len(distances) > 1:
            if current_distance - distances[-1] < 0:
                r_plus += 2
            elif current_distance - distances[-1] > 0:
                r_plus = 0
        reward += r_plus
        if obstacle_distance_y_down ** 2 < obstacle_distance_y_up ** 2:
            if obstacle_distance_y_down ** 2 >= 9:
                obstacle_y = -2
            else:
                obstacle_y = -1
        elif obstacle_distance_y_down ** 2 > obstacle_distance_y_up ** 2:
            if obstacle_distance_y_up ** 2 >= 9:
                obstacle_y = 2
            else:
                obstacle_y = 1
        else:
            obstacle_y = 0
        if obstacle_distance_x_right ** 2 < obstacle_distance_x_left ** 2:
            if obstacle_distance_x_right ** 2 >= 9:
                obstacle_x = 2
            else:
                obstacle_x = 1
        elif obstacle_distance_x_right ** 2 > obstacle_distance_x_left ** 2:
            if obstacle_distance_x_left ** 2 >= 9:
                obstacle_x = -2
            else:
                obstacle_x = -1
        else:
            obstacle_x = 0
        if score > 0:
            for chunk in range(len(snake_body)):
                if snake.head.xcor() == snake_body[chunk].head.xcor() or \
                        snake.head.ycor() == snake_body[chunk].head.ycor():
                    over = True
                    reward = -1000
                if snake.head.xcor() == snake_body[chunk].head.xcor():
                    if snake.head.ycor() < snake_body[chunk].head.ycor():
                        obstacle_distance_y_up = (snake_body[chunk].head.ycor() - snake.head.ycor()) / scalar
                        obstacle_y = -1
                    if snake.head.ycor() > snake_body[chunk].head.ycor():
                        obstacle_distance_y_down = (snake.head.ycor() - snake_body[chunk].head.ycor()) / scalar
                        obstacle_y = 1
                if snake.head.ycor() == snake_body[chunk].head.ycor():
                    if snake.head.xcor() > snake_body[chunk].head.xcor():
                        obstacle_distance_x_right = (snake.head.xcor() - snake_body[chunk].head.xcor()) / scalar
                        obstacle_x = 1
                    if snake.head.xcor() < snake_body[chunk].head.xcor():
                        obstacle_distance_x_left = (snake_body[chunk].head.xcor() - snake.head.xcor()) / scalar
                        obstacle_x = -1
        distances.append(current_distance)
        state = [int(x_dir), int(y_dir), int(obstacle_x), int(obstacle_y), score]
        action_dec = random.random()
        action = np.argmax(q_table[list_possible_states.index(state)])
        if action_dec < learning_rate:
            action = random.randint(0, 3)
        if len(snake_body) > 0:
            for i in range(len(snake_body)):
                snake_body[-(i + 1)].head.goto(x_co_ords[(- (i + 1))], y_co_ords[- (i + 1)])
        if snake.head.xcor() >= 280 or snake.head.xcor() <= -280:
            reward = -1000
            over = True
        if snake.head.ycor() >= 280 or snake.head.ycor() <= -280:
            reward = -1000
            over = True
        if snake.head.distance(snack.snack) < 20:
            snack.set_loc()
            snake_body.append(Snake("orange"))
            score += 1
            reward = 1000
        snake.move(action)
        x_diff = - 1 * ((snake.head.xcor() / scalar) - (snack.snack.xcor() / scalar))
        y_diff = - 1 * ((snake.head.ycor() / scalar) - (snack.snack.ycor() / scalar))
        if x_diff > 0:
            x_dir = 1
        elif x_diff < 0:
            x_dir = -1
        else:
            x_dir = 0
        if y_diff > 0:
            y_dir = 1
        elif y_diff < 0:
            y_dir = -1
        else:
            y_dir = 0
        if obstacle_distance_y_down**2 < obstacle_distance_y_up**2:
            if obstacle_distance_y_down**2 >= 9:
                obstacle_y = -2
            else:
                obstacle_y = -1
        elif obstacle_distance_y_down**2 > obstacle_distance_y_up**2:
            if obstacle_distance_y_up ** 2 >= 9:
                obstacle_y = 2
            else:
                obstacle_y = 1
        else:
            obstacle_y = 0
        if obstacle_distance_x_right**2 < obstacle_distance_x_left**2:
            if obstacle_distance_x_right ** 2 >= 9:
                obstacle_x = 2
            else:
                obstacle_x = 1
        elif obstacle_distance_x_right**2 > obstacle_distance_x_left**2:
            if obstacle_distance_x_left ** 2 >= 9:
                obstacle_x = -2
            else:
                obstacle_x = -1
        else:
            obstacle_x = 0
        if score > 0:
            for chunk in range(len(snake_body)):
                if snake.head.xcor() == snake_body[chunk].head.xcor() or \
                        snake.head.ycor() == snake_body[chunk].head.ycor():
                    over = True
                    reward = -1000
                if snake.head.xcor() == snake_body[chunk].head.xcor():
                    if snake.head.ycor() < snake_body[chunk].head.ycor():
                        obstacle_distance_y_up = (snake_body[chunk].head.ycor() - snake.head.ycor()) / scalar
                        obstacle_y = -1
                    if snake.head.ycor() > snake_body[chunk].head.ycor():
                        obstacle_distance_y_down = (snake.head.ycor() - snake_body[chunk].head.ycor()) / scalar
                        obstacle_y = 1
                if snake.head.ycor() == snake_body[chunk].head.ycor():
                    if snake.head.xcor() > snake_body[chunk].head.xcor():
                        obstacle_distance_x_right = (snake.head.xcor() - snake_body[chunk].head.xcor()) / scalar
                        obstacle_x = 1
                    if snake.head.xcor() < snake_body[chunk].head.xcor():
                        obstacle_distance_x_left = (snake_body[chunk].head.xcor() - snake.head.xcor()) / scalar
                        obstacle_x = -1
        distances.append(current_distance)
        if len(snake_body) > 0:
            for i in range(len(snake_body)):
                snake_body[-(i + 1)].head.goto(x_co_ords[(- (i + 1))], y_co_ords[- (i + 1)])
        if snake.head.xcor() >= 280 or snake.head.xcor() <= -280:
            reward = -1000
            over = True
        if snake.head.ycor() >= 280 or snake.head.ycor() <= -280:
            reward = -1000
            over = True
        if snake.head.distance(snack.snack) < 20:
            snack.set_loc()
            snake_body.append(Snake("orange"))
            score += 1
            reward = 1000
        new_state = [int(x_dir), int(y_dir), int(obstacle_x), int(obstacle_y), score]
        max_future_q = np.max(q_table[list_possible_states.index(new_state)])
        current_q = q_table[list_possible_states.index(state), action]
        new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount * max_future_q)
        q_table[list_possible_states.index(state), action] = new_q
        p += 1
        print(f"State: {state} | Action: {action} | Reward: {reward} "
              f"| Iteration: {p} | Learning rate: {learning_rate} | Episode: {a + 1}")
        if p == epoch:
            over = True
        win.update_window()
    a += 1
    if learning_rate > 0.05:
        learning_rate -= 0.05
    win.win.clear()
np.savetxt('q_table_snake.csv', q_table, delimiter=',')
