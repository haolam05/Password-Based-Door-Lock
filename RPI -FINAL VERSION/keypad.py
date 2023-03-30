import time
import GPIO as MyGPIO

ROWS         = { "R1":16, "R2":18, "R3":22, "R4":36 }
COLS         = { "C1":11, "C2":13, "C3":15, "C4":29 }
digits       = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
keys         = [
                    ["1", "2", "3", "A"],
                    ["4", "5", "6", "B"],
                    ["7", "8", "9", "C"],
                    ["*", "0", "#", "D"]
                ]


def take_input():
    while True:
        res = scan_row(ROWS["R1"], keys[0])
        if res != False:
            return res
        res = scan_row(ROWS["R2"], keys[1])
        if res != False:
            return res
        res = scan_row(ROWS["R3"], keys[2])
        if res != False:
            return res
        res = scan_row(ROWS["R4"], keys[3])
        if res != False:
            return res


def scan_row(row, chars):
    MyGPIO.write(row, 1)
    res = False

    if (MyGPIO.read(COLS["C1"])):
        res = chars[0]
    if (MyGPIO.read(COLS["C2"])):
        res = chars[1]
    if (MyGPIO.read(COLS["C3"])):
        res = chars[2]
    if (MyGPIO.read(COLS["C4"])):
        res = chars[3]

    MyGPIO.write(row, 0)
    return res

