import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # GPIO on the plug
GPIO.setwarnings(False)


def set_pins(pins, direction):
    for key in pins:
        if direction == "IN":
            GPIO.setup(pins[key], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif direction == "OUT":
            GPIO.setup(pins[key], GPIO.OUT)


def read(pin):
    return GPIO.input(pin)


def write(pin, state):
    GPIO.output(pin, state)
