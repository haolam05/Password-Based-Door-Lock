from time import sleep
import random
import Gotify_Notification as Notification
import GPIO                as MyGPIO
import SMTP_Gmail          as Gmail
import LCD                 as LCD
import password            as Password
import keypad              as Keypad
import setup               as SetUp
import lock                as Lock
import face_recognition    as Face_Recog

# Initialize states and parameters to be used
save_pswd          = ["?"]#, "?", "?", "?"]
save_salt          = [b'0']
test_pswd          = ["?"] #, "?", "?", "?"]
attempts           = 0
ALLOWED_ATTEMPTS   = 3
ALLOWED_NUM_DIGITS = 4
STATES             = { "lock_screen":0, "face":1, "start":2, "take_input":3, "eval_input":4, "report":5, "LOCKED":6, "current":0 }
SERVO              = { "lock_control":31 }

# Set rows and columns of keypad to input; Set Servo control signal pin to output
MyGPIO.set_pins(Keypad.ROWS, "OUT")
MyGPIO.set_pins(Keypad.COLS, "IN")
MyGPIO.set_pins(SERVO, "OUT")

# Customer enters password before installing. Customer needs to contact company for changing password.
SetUp.set_pswd(save_pswd, save_salt, True)

# FSM
while True:
    # OUTPUTS
    if (STATES["current"] == STATES["lock_screen"]):
        Lock.closes(SERVO["lock_control"])
        LCD.lock_screen()
        attempts = 0
    elif (STATES["current"] == STATES["face"]):
        is_recognized = Face_Recog.greet_if_saw_members()
    elif (STATES["current"] == STATES["start"]):
        if attempts < ALLOWED_ATTEMPTS:
            LCD.print_prompting_msg()
    elif (STATES["current"] == STATES["take_input"]):
        SetUp.set_pswd(test_pswd, save_salt)
    elif (STATES["current"] == STATES["eval_input"]):
        if (Password.evaluate(save_pswd, test_pswd, save_salt)):
            Lock.opens(SERVO["lock_control"])
            Lock.closes(SERVO["lock_control"])
            LCD.print_welcome_msg()
            LCD.print_close_door_msg()
        else:
            Notification.send()
            LCD.print_warning_msg()
            attempts = attempts + 1
    elif (STATES["current"] == STATES["report"]):
        Notification.send("Intruder photo is captured. Check your email!")
        rand = random.randrange(0, 10**ALLOWED_NUM_DIGITS)
        Gmail.send("Intruder photo is captured. New password is generated: " + str(rand))
     
#         for i in range(len(save_pswd)):  # saved random generated password
#             save_pswd[len(save_pswd)-1-i] = Password.set(rand % 10)
#             rand = int(rand/10)
        save_salt[0] = Password.create_salt();
        save_pswd[0] = Password.set(rand, save_salt[0]);
    elif (STATES["current"] == STATES["LOCKED"]):
        attempts = attempts - 1
        LCD.print_report_msg()
        LCD.print_countdown_timer(Password.WAIT_DURATION)  # if attempts >= ALLOWED_ATTEMPTS, screen is locked for given duration

    # STATE TRANSITIONS
    if (STATES["current"] == STATES["lock_screen"]):
        if Keypad.take_input() == "#":
            STATES["current"] = STATES["start"]
        elif Keypad.take_input() == "D":  # activate face recognition
            STATES["current"] = STATES["face"]
    elif (STATES["current"] == STATES["face"]):
        STATES["current"] = STATES["start"] if is_recognized else STATES["face"]
    elif (STATES["current"] == STATES["start"]):
        STATES["current"] = (STATES["report"] if attempts >= ALLOWED_ATTEMPTS else STATES["take_input"])
    elif (STATES["current"] == STATES["take_input"]):
        STATES["current"] = STATES["eval_input"]
    elif (STATES["current"] == STATES["eval_input"]):
        if (Password.evaluate(save_pswd, test_pswd, save_salt)):
            STATES["current"] = STATES["lock_screen"]
        else:
            STATES["current"] = STATES["start"]
    elif (STATES["current"] == STATES["report"]):
        STATES["current"] = STATES["LOCKED"]
    elif (STATES["current"] == STATES["LOCKED"]):
        STATES["current"] = STATES["start"]