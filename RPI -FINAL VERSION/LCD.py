import sys
sys.path.append('/home/haolam05/Desktop/475/lcd')
from lcd      import drivers
from time     import sleep
from datetime import datetime

display = drivers.Lcd()

def print_close_door_msg():
    display.lcd_clear()
    display.lcd_display_string("Push button to", 1)
    display.lcd_display_string("close the door.", 2)
    sleep(2)
    
def print_report_msg():
    print_custom_msg("911 is coming!!")
    flash_backlight_OnOff(3)

def lock_screen():
    display.lcd_clear()
    display.lcd_display_string(datetime.now().strftime("%A"), 1)
    display.lcd_display_string(str(datetime.now()), 2)

def print_pswd(digit):
    str = ("    " if digit == 0 else (
           "*   " if digit == 1 else (
           "**  " if digit == 2 else (
           "*** " if digit == 3 else (
           "****" if digit == 4 else (
        ))))))

    display.lcd_display_string(str, 2)

def print_prompting_msg():
    print_custom_msg("Enter Password:")

def print_custom_msg(msg, line=1):
    display.lcd_clear()
    display.lcd_display_string(msg, line)
    sleep(2)

def print_welcome_msg():
    display.lcd_clear()
    display.lcd_display_string("ACCESS GRANTED!", 1)
    display.lcd_display_string("Welcome Home!", 2)
    sleep(2)
    display.lcd_clear()
    
def print_warning_msg():
    display.lcd_clear()
    display.lcd_display_string("WRONG PASSWORD!", 1)
    display.lcd_display_string("Try again!", 2)
    sleep(2)                                          # Waiting for backlight toggle
    flash_backlight_OnOff(3)
    display.lcd_clear()

def flash_backlight_OnOff(times):
    for i in range(times):
        display.lcd_backlight(1)                       # Make sure backlight is on / turn on
        sleep(0.5)                                     # Waiting for backlight toggle
        display.lcd_backlight(0)                       # Turn backlight off
        sleep(0.5)                                     # Waiting for turning backlight on again
        display.lcd_backlight(1)                       # Turn backlight on again

def print_countdown_timer(time):
    t = time
    while t:
        mins, secs = divmod(t, 60)
        display.lcd_display_string('{:02d}:{:02d}'.format(mins, secs), 2)
        sleep(1)
        t = t - 1