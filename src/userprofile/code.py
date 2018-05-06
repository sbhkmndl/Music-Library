import random
import string

chars = string.ascii_lowercase + string.digits + string.ascii_uppercase


def code_generator(size=10):

    return "".join(random.choice(chars) for _ in range(size))
