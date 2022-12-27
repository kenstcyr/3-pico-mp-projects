from machine import ADC, Timer
from st7920 import st7920

display_temp = ""

# Initialize LCD on SPI0
lcd = st7920.Screen(rst=0, cs=5)

# Enable graphics mode on the LCD and clear the screen
lcd.graphics_mode()
lcd.clear()

def tick(timer):
    global display_temp

    # Read the temperature from Pico's onboard sensor
    temp = ADC(4).read_u16()

    # Convert the temperature
    volt = temp * 3.3 / 65535
    temp_c = 27 - (volt - 0.706)/0.001721
    temp_f = (temp_c * 9 / 5) + 32

    # Update display string
    display_temp = str(round(temp_f, 1))

# Create and start a timer
timer = Timer(-1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=tick)

# Display Loop
while True:
    lcd.clear()
    lcd.rect(28, 14, 100, 46)
    lcd.rect(26, 12, 102, 48)
    lcd.put_text("Current", 43, 17)
    lcd.put_text("Temperature", 31, 26)
    lcd.put_text(display_temp + " F", 46, 36)
    lcd.circle(73, 37, 1)
    lcd.redraw()
