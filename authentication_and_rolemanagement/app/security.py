import random
import string


def generate_captcha():
    letters = string.ascii_letters
    captcha_text = "".join(random.choice(letters) for i in range(6))
    return captcha_text


def verify_captcha(user_input, actual_captcha):
    return user_input == actual_captcha
