from machine import Pin, PWM
from utime import sleep

buzzer = PWM(Pin(2, mode=Pin.OUT))
sound = 0
note = 262

# Setup keys
button_C = Pin(3, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_D = Pin(4, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_E = Pin(5, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_F = Pin(6, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_G = Pin(7, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_A = Pin(8, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_B = Pin(9, mode=Pin.IN, pull=Pin.PULL_DOWN)
button_C2 = Pin(10, mode=Pin.IN, pull=Pin.PULL_DOWN)

while True:
    sound = 32768

    if button_C.value(): note = 262
    elif button_D.value(): note = 294
    elif button_E.value(): note = 330
    elif button_F.value(): note = 349
    elif button_G.value(): note = 392
    elif button_A.value(): note = 440
    elif button_B.value(): note = 494
    elif button_C2.value(): note = 523
    else:
        sound = 0

    buzzer.freq(note)
    buzzer.duty_u16(sound)