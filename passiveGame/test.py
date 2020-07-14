import shlex, subprocess

import sys

import random

import time

args = shlex.split('python3 passiveGame.py')

sys.path.insert(0, '..')

import constants as c

# ------------ Main function --------------------

p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

while True:

    time.sleep(1)

    randomColor = random.choice( c.colors )

    p.stdin.write( bytearray(randomColor+'\n' , encoding="utf-8") )

    p.stdin.flush()

