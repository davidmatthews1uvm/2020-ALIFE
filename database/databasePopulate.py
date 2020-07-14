#!/usr/bin/python3
import sys
import os

sys.path.insert(0, '..')

from database.database import DATABASE

if __name__ == "__main__":
    d = DATABASE()
    d.Populate()
