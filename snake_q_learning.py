#  for the trained agent, please download the 'snake_q_table.csv' file. 
import turtle
import random
import time
import numpy as np
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


def get_state(snke, snke_body, snck, scre, sclr):
    s_1 = 0
    s_2 = [0, 0, 0, 0]
    if (- 1 * ((snke.head.xcor() / sclr) - (snck.snack.xcor() / sclr))) > 0:
        x_dir = 1
    elif (- 1 * ((snke.head.xcor() / sclr) - (snck.snack.xcor() / sclr))) < 0:
        x_dir = -1
    else:
        x_dir = 0
    if (- 1 * ((snke.head.ycor() / sclr) - (snck.snack.ycor() / sclr))) > 0:
        y_dir = 1
    elif (- 1 * ((snke.head.ycor() / sclr) - (snck.snack.ycor() / sclr))) < 0:
        y_dir = -1
    else:
        y_dir = 0
    if y_dir == 1 and x_dir == 0:
        s_1 = 1
    elif y_dir == 1 and x_dir == 1:
        s_1 = 2
    elif y_dir == 0 and x_dir == 1:
        s_1 = 3
    elif y_dir == -1 and x_dir == 1:
        s_1 = 4
    elif y_dir == -1 and x_dir == 0:
        s_1 = 5
    elif y_dir == -1 and x_dir == -1:
        s_1 = 6
    elif y_dir == 0 and x_dir == -1:
        s_1 = 7
    elif y_dir == 1 and x_dir == -1:
        s_1 = 8
    if snke.head.ycor() >= 250:
        s_2[0] = 1
    if snke.head.xcor() >= 250:
        s_2[1] = 1
    if snke.head.ycor() <= -250:
        s_2[2] = 1
    if snke.head.xcor() <= -250:
        s_2[3] = 1
    if scre > 0:
        for chnk in range(len(snke_body)):
            if snke.head.distance(snke_body[chnk].head) < 40:
                if (- 1 * ((snke.head.xcor() / sclr) - (snke_body[chnk].head.xcor() / sclr))) > 0:
                    s_2[1] = 1
                elif (- 1 * ((snke.head.xcor() / sclr) - (snke_body[chnk].head.xcor() / sclr))) < 0:
                    s_2[3] = 1
                if (- 1 * ((snke.head.ycor() / sclr) - (snke_body[chnk].head.ycor() / sclr))) > 0:
                    s_2[0] = 1
                elif (- 1 * ((snke.head.ycor() / sclr) - (snke_body[chnk].head.ycor() / sclr))) < 0:
                    s_2[2] = 1
    state_instance = [s_1, scre]
    state_instance.extend(s_2)
    return state_instance


def create_possible_states():
    poss_states = []
    num = 1
    for first in range(0, 9):
        for scor in range(0, 20):
            for s_2_1 in range(0, 2):
                for s_2_2 in range(0, 2):
                    for s_2_3 in range(0, 2):
                        for s_2_4 in range(0, 2):
                            poss_states.append([first, scor, s_2_1, s_2_2, s_2_3, s_2_4])
                            print(f"Iteration {num}: State: {poss_states[-1]}")
                            num += 1
    return poss_states


learning_rate = 0.1
list_possible_states = create_possible_states()
dim = len(list_possible_states)

# q_table = np.random.uniform(low=-2, high=0, size=(dim, 4))
q_table = np.loadtxt('snake_q_table.csv', delimiter=',')
episodes = 600
actions_n = 4
epoch = 5000
scalar = 20
a = 0
discount = 0.9
#  tweak parameters
while a < episodes:
    win = Window("Snake", "black", 600, 600, a+1, learning_rate)
    snake = Snake("red")
    snack = Snack()
    snack.set_loc()
    x_co_ords = []
    y_co_ords = []
    snake_body = []
    distances = []
    over = False
    score = 0
    p = 0
    r_plus = 0
    while over is False:
        if (a + 1) % 200 == 0:
            time.sleep(0.05)
        # time.sleep(0.05)
        reward = 0
        x_co_ords.append(snake.head.xcor())
        y_co_ords.append(snake.head.ycor())
        current_distance = math.sqrt((- 1 * ((snake.head.xcor() / scalar) - (snack.snack.xcor() / scalar))) ** 2 +
                                     (- 1 * ((snake.head.ycor() / scalar) - (snack.snack.ycor() / scalar))) ** 2)
        #  higher reward closer snake gets
        distances.append(current_distance)
        state = get_state(snake, snake_body, snack, score, scalar)
        action_dec = random.random()
        action = np.argmax(q_table[list_possible_states.index(state)])
        if action_dec < learning_rate:
            action = random.randint(0, 3)
        snake.move(action)
        if score > 0:
            for chunk in range(len(snake_body)):
                if snake.head.distance(snake_body[chunk].head) < 20:
                    over = True
                    reward -= 1000
        if len(distances) > 1:
            if current_distance - distances[-1] < 0:
                r_plus = 0
            elif current_distance - distances[-1] > 0:
                r_plus -= 2
        reward += r_plus
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
        if len(snake_body) > 0:
            for i in range(len(snake_body)):
                snake_body[-(i + 1)].head.goto(x_co_ords[(- (i + 1))], y_co_ords[- (i + 1)])
        distances.append(current_distance)
        if len(snake_body) > 0:
            for i in range(len(snake_body)):
                snake_body[-(i + 1)].head.goto(x_co_ords[(- (i + 1))], y_co_ords[- (i + 1)])
        if snake.head.xcor() >= 280 or snake.head.xcor() <= -280:
            reward -= 1000
            over = True
        if snake.head.ycor() >= 280 or snake.head.ycor() <= -280:
            reward -= 1000
            over = True
        if snake.head.distance(snack.snack) < 20:
            snack.set_loc()
            snake_body.append(Snake("orange"))
            score += 1
            reward += 1000
        # reward -= p
        new_state = get_state(snake, snake_body, snack, score, scalar)
        max_future_q = np.max(q_table[list_possible_states.index(new_state)])
        current_q = q_table[list_possible_states.index(state), action]
        new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount * max_future_q)
        q_table[list_possible_states.index(state), action] = new_q
        p += 1
        print(f"State: {state} | Action: {action} | Reward: {reward} "
              f"| Iteration: {p} | Learning rate: {learning_rate} | Episode: {a + 1}")
        # if p == epoch:
        #     over = True
        win.update_window()
    a += 1
    if learning_rate > 0.05:
        learning_rate -= 0.01
    win.win.clear()
np.savetxt('snake_q_table.csv', q_table, delimiter=',')
print("Q table saved. Iterations complete. ")
