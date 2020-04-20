import turtle
import numpy as np
import random


class Window:
    def __init__(self, title, background_colour, window_width, window_height):
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
        self.pen.goto(-200, 250)
        self.pen.write("Graham, the RL AI", align="center", font=("Courier", 24, "normal"))
        self.pen.goto(150, 250)
        self.pen.write("John, classic, stinky, bot", align="center", font=("Courier", 24, "normal"))

    def update_window(self):
        self.win.update()


class Paddle:
    def __init__(self, paddle_colour, object_x, object_y):
        self.obj = turtle.Turtle()
        self.obj.speed(0)
        self.obj.shape("square")
        self.obj.color(paddle_colour)
        self.obj.shapesize(stretch_len=1, stretch_wid=5)
        self.obj.penup()
        self.obj.goto(object_x, object_y)
        self.x = self.obj.xcor()
        self.y = self.obj.ycor()
        self.y = object_y

    def move_up(self):
        y = self.obj.ycor()
        y += 30
        self.obj.sety(y)

    def move_down(self):
        y = self.obj.ycor()
        y += -30
        self.obj.sety(y)

    def stinky_auto_paddle(self, ball_y):
        move_val = 0
        if self.obj.ycor() < ball_y:
            move_val = 10
        elif self.obj.ycor() > ball_y:
            move_val = -10
        new_y = self.obj.ycor()
        new_y += move_val
        self.obj.sety(new_y)

    def rl_auto_paddle(self, action_rl):
        move_val = 0
        if action_rl == 0:
            move_val -= 10
        elif action_rl == 1:
            move_val += 10
        new_y = self.obj.ycor()
        new_y += move_val
        self.obj.sety(new_y)


class Ball:
    def __init__(self, paddle_colour, object_x, object_y):
        self.obj = turtle.Turtle()
        self.obj.speed(0)
        self.obj.shape("square")
        self.obj.color(paddle_colour)
        self.obj.penup()
        self.obj.goto(object_x, object_y)
        self.x = self.obj.xcor()
        self.y = self.obj.ycor()
        self.y = object_y
        self.possible_beginning_x_direction = [1, -1]
        self.possible_beginning_y_direction = [1, -1]
        self.dys = [2, 4, 6, 8]
        self.dx = 10 * self.possible_beginning_x_direction[random.randint(0, 1)]
        self.dy = self.possible_beginning_y_direction[random.randint(0, 1)]\
            * self.dys[random.randint(0, len(self.dys) - 1)]
        self.over = False
        self.who_won = ""

    def move(self, paddle_a_y, paddle_b_y):
        self.who_won = ""
        self.obj.setx(self.obj.xcor() + self.dx)
        self.obj.sety(self.obj.ycor() + self.dy)
        if self.obj.ycor() > 290 or self.obj.ycor() < -290:
            self.dy *= -1
        if self.obj.xcor() > 350:
            self.dx = 0
            self.dy = 0
            print("Orange player wins!")
            self.who_won = "orange"
            self.over = True
        if self.obj.xcor() < -350:
            self.dx = 0
            self.dy = 0
            print("Yellow player wins!")
            self.who_won = "yellow"
            self.over = True
        if self.obj.xcor() > 340 and \
                ((paddle_b_y - 70) < self.obj.ycor() < (paddle_b_y + 70)):
            self.dx *= -1
            self.dy *= -1
        if self.obj.xcor() < -340 and \
                ((paddle_a_y - 70) < self.obj.ycor() < (paddle_a_y + 70)):
            self.dx *= -1
            self.dy *= -1
            self.who_won = "nice hit!"


def create_possible_states():
    poss_states = []
    num = 1
    for first in range(-1, 2):
        poss_states.append([first])
        print(f"Iteration {num}: State: {poss_states[-1]}")
        num += 1
    return poss_states


def get_state(paddle, ball_):
    x = int
    if ball_.obj.ycor() > paddle.obj.ycor():
        x = 1
    elif ball_.obj.ycor() < paddle.obj.ycor():
        x = -1
    if -20 < ball_.obj.ycor() - paddle.obj.ycor() < 20:
        x = 0
    return x


def get_reward(state_, act, reward_, ball_):
    if state_ == 1 and act == 1:
        reward_ += 10
    if state_ == -1 and act == 0:
        reward_ += 10
    if state_ == 0 and act == 2:
        reward_ += 20
    if ball_.who_won == "nice hit!":
        reward_ += 50
    return reward_


def step(paddle_1, paddle_2, _ball, action_):
    paddle_1.rl_auto_paddle(action_)
    paddle_2.stinky_auto_paddle(_ball.obj.ycor())
    _ball.move(paddle_1.obj.ycor(), paddle_2.obj.ycor())


def get_action(q, states_list, _state):
    _action = np.argmax(q[states_list.index(_state)])
    decide = random.random()
    if decide < learning_rate:
        _action = random.randint(0, 2)
    return _action


possible_states = create_possible_states()
q_table = np.random.uniform(low=-2, high=0, size=(len(possible_states), 3))

epochs = 2000
learning_rate = 0.1
discount = 0.9

episodes = 20
ep = 0
while ep < episodes:
    window = Window("Pong", "black", 800, 600)
    paddle_a = Paddle("orange", -350, 0)
    paddle_b = Paddle("yellow", 350, 0)
    ball = Ball("white", 0, 0)
    window.pen.goto(0, 175)
    window.pen.write(f"Iteration: {ep + 1}/{episodes}", align="center", font=("Courier", 16, "normal"))
    m = 0
    reward = 0
    while ball.over is False:
        window.update_window()
        state_1 = get_state(paddle_a, ball)
        state = [state_1]
        action = np.argmax(q_table[possible_states.index(state)])
        if random.random() < learning_rate:
            action = random.randint(0, 2)
        step(paddle_a, paddle_b, ball, action)
        reward = get_reward(state_1, action, reward, ball)
        state_1 = get_state(paddle_a, ball)
        new_state = [state_1]
        print(f"State: {new_state} | Learning rate: {learning_rate} | Action: {action} | Reward: {reward}")
        max_future_q = np.max(q_table[possible_states.index(new_state)])
        current_q = q_table[possible_states.index(state), action]
        new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount * max_future_q)
        q_table[possible_states.index(state), action] = new_q
        m += 1
        if m >= epochs:
            m = 0
            ball.over = True
    window.win.clear()
    ep += 1
