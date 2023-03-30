from time import sleep
import LCD      as LCD
import keypad   as Keypad
import password as Password

pswd_len = 4


def set_pswd(pswd, salt, setup=False):
    if (setup):
        LCD.print_custom_msg("New password:")

    i = 0
    val = ''
    while i < pswd_len:
        res = Keypad.take_input()

        if res == "*":  # delete
            # pswd[i] = "?"
            i = i - (1 if i > 0 else 0)
            val = val[:-1]
        elif res in Keypad.digits:
            val = val + res
            i = i + 1

        LCD.print_pswd(i)
        sleep(1)

    if (setup):
        salt[0] = Password.create_salt()
    pswd[0] = Password.set(int(val), salt[0])

    if (setup):
        LCD.print_custom_msg("Password Saved!")
