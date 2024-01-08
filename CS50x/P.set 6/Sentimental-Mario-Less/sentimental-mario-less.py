# TODO
from cs50 import get_int

while True:
    a = get_int("Height: ")

    if a >= 1 and a <= 8:
        break
    else:
        continue

for i in range(a):
    print(" " * (a - (i + 1)) + "#" * (i + 1))
