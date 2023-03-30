import GPIO as MyGPIO

def opens(pin):
    MyGPIO.write(pin, 1)

def closes(pin):
    MyGPIO.write(pin, 0)
