import os
from rich import print
from rich import color
import random

colors = sorted((v, k) for k, v in color.ANSI_COLOR_NAMES.items())


def random_color():
    return random.choice(colors)


for key, value in os.environ.items():
    color = random_color()[1]
    color2 = random_color()[1]
    print(f"[{color}]{key}={value}[/{color}]")
