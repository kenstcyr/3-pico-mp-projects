import st7920
from machine import ADC, Timer, Pin, PWM
from brick import Brick
from time import sleep_ms

buzzer = PWM(Pin(15, mode=Pin.OUT))
buzzer.duty_u16(0)
buzzer.freq(262)

button = Pin(13, mode=Pin.IN, pull=Pin.PULL_DOWN)
lastButton = False
currentButton = False

ball_alive = False
ball_x = 0
ball_y = 30
ball_x_dir = 1
ball_y_dir = -1
bricks = [
            Brick(1, 2), Brick(15, 2), Brick(29, 2), Brick(43, 2), Brick(57, 2), Brick(71, 2), Brick(85, 2), Brick(99, 2), Brick(113, 2),
            Brick(1, 7), Brick(15, 7), Brick(29, 7), Brick(43, 7), Brick(57, 7), Brick(71, 7), Brick(85, 7), Brick(99, 7), Brick(113, 7),
            Brick(1, 12), Brick(15, 12), Brick(29, 12), Brick(43, 12), Brick(57, 12), Brick(71, 12), Brick(85, 12), Brick(99, 12), Brick(113, 12),
            Brick(1, 17), Brick(15, 17), Brick(29, 17), Brick(43, 17), Brick(57, 17), Brick(71, 17), Brick(85, 17), Brick(99, 17), Brick(113, 17),
            Brick(1, 22), Brick(15, 22), Brick(29, 22), Brick(43, 22), Brick(57, 22), Brick(71, 22), Brick(85, 22), Brick(99, 22), Brick(113, 22)
        ]

x_pos = 0
y_pos = 62
paddle_w = 10
sound_hit = False

div = 65535 // (128 - paddle_w)

lcd = st7920.Screen(cs=5, rst=0)

def tick(timer):
    # Update the ball position
    update_ball_pos()

    # Bounce ball off wall
    bounce_wall()

    # Bounce ball of paddle
    bounce_paddle()

    # Kill the player
    kill_ball()

def debounce(last):
    global button
    current = button.value()
    if last != current:
        sleep_ms(5)
        current = button.value()
    return current

def process_sound(timer2):
    global buzzer, sound_hit
    if sound_hit:
        buzzer.duty_u16(32768)
        sleep_ms(100)
        buzzer.duty_u16(0)
        sound_hit = False
                
def update_ball_pos():
    global ball_x, ball_y, ball_x_dir, ball_y_dir, ball_alive, sound_hit, buzzer

    if ball_alive:
        ball_x += ball_x_dir
        ball_y += ball_y_dir
    
        # Did ball hit brick?
        for b in bricks:
            if b.visible:
                if (ball_x == b.x + 12 or ball_x == b.x) and (ball_y <= b.y + 4 and ball_y >= b.y):
                    ball_x_dir *= -1
                    b.visible = False
                    buzzer.freq(262)
                    sound_hit = True
                if (ball_y == b.y + 4 or ball_y == b.y) and (ball_x <= b.x + 12 and ball_x >= b.x):
                    ball_y_dir *= -1
                    b.visible = False
                    buzzer.freq(262)
                    sound_hit = True

    else:
        ball_x = x_pos + (paddle_w // 2)
        ball_y = y_pos - 1

def bounce_wall():
    global ball_x, ball_y, ball_x_dir, ball_y_dir, ball_alive
    if ball_alive:
        if ball_x == 127 or ball_x == 0:
            ball_x_dir *= -1
        if ball_y == 0:
            ball_y_dir *= -1

def bounce_paddle():
    global ball_x, ball_y, ball_y_dir, ball_alive, buzzer, sound_hit
    if ball_alive:
        if ball_y == 61 and ball_x >= x_pos and ball_x <= x_pos + paddle_w:
            ball_y_dir *= -1
            buzzer.freq(600)
            sound_hit = True

def kill_ball():
    global ball_y, ball_alive
    if ball_alive:
        if (ball_y > 61):
            buzzer.duty_u16(32768)
            buzzer.freq(440)
            sleep_ms(500)
            buzzer.freq(349)
            sleep_ms(500)
            buzzer.freq(392)
            sleep_ms(500)
            buzzer.duty_u16(0)
            ball_alive = False

def process_button():
    global ball_alive, button, ball_y_dir
    if ball_alive == False:
        if button.value():
            ball_y_dir = -1
            ball_alive = True

def draw_bricks():
    for b in bricks:
        if b.visible:
            lcd.fill_rect(b.x, b.y, b.x+12, b.y+4)

# Create and start the game logic timer
timer = Timer(-1)
timer.init(period=80, mode=Timer.PERIODIC, callback=tick)

# Create and start the sound effect timer
timer2 = Timer(-1)
timer2.init(period=100, mode=Timer.PERIODIC, callback=process_sound)

while True:
    # Check the status of the launch button, and launch the ball
    currentButton = debounce(lastButton)
    if lastButton == False and currentButton == True:
        process_button()
    lastButton = currentButton

    lcd.clear()

    # Read the potentiometer and update the paddle position
    pot_val = ADC(0).read_u16()
    x_pos = pot_val // div

    # Draw the ball
    lcd.plot(ball_x, ball_y)

    # Draw the bricks
    draw_bricks()

    # Draw the paddle
    lcd.line(x_pos, y_pos, x_pos + paddle_w, y_pos)

    # Redraw the screen
    lcd.redraw()