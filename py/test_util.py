import os
import sys

BOLD = "\u001b[1m"
GRAY = "\u001b[38;5;248m"
CYAN = "\u001b[36m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
RESET = "\u001b[0m"


def fail(message):
    print(RED + BOLD + "FAIL: " + RESET + message)
    sys.exit(1)


def check(condition, message):
    if not condition:
        fail(message)
