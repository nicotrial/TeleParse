# -*- coding: utf-8 -*-

import sys, os, time
from time import sleep
import random

RED   = "\033[0;31m"  
BLUE  = "\033[0;34m"
CYAN  = "\033[0;36m"
GREEN = "\033[0;32m"
RED2  =  "\033[0;41m"
BRED   = "\033[1;31m"  
BBLUE  = "\033[1;34m"
BCYAN  = "\033[1;36m"
BGREEN = "\033[1;32m"
BRED2  =  "\033[1;41m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def hackerPrint(msg, type="ERROR", bold=False, speed=0.03):

    if type is "ERROR":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stdout.write(RED + char + RESET)
                sys.stdout.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stdout.write(BRED + char + RESET)
                sys.stdout.flush()

    if type is "HEAVY":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stdout.write(CYAN + char + RESET)
                sys.stdout.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stdout.write(BCYAN + char + RESET)
                sys.stdout.flush()

    if type is "GOOD":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stdout.write(GREEN + char + RESET)
                sys.stdout.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stdout.write(BGREEN + char + RESET)
                sys.stdout.flush()

    if type is "VERYBAD":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stdout.write(RED2 + char + RESET)
                sys.stdout.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stdout.write(BRED2 + char + RESET)
                sys.stdout.flush()

    if type is "IRHUMAN":
        if not bold:
            for char in msg:
                sleep(random.uniform(0.05, 0.4))
                sys.stdout.write(GREEN + char + RESET)
                sys.stdout.flush()
        else:         
            for char in msg:
                sleep(random.uniform(0.05, 0.4))
                sys.stdout.write(BGREEN + char + RESET)
                sys.stdout.flush()

def hackerPrintErr(msg, type="ERROR", bold=False, speed=0.03):

    if type is "ERROR":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stderr.write(RED + char + RESET)
                sys.stderr.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stderr.write(BRED + char + RESET)
                sys.stderr.flush()

    if type is "HEAVY":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stderr.write(CYAN + char + RESET)
                sys.stderr.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stderr.write(BCYAN + char + RESET)
                sys.stderr.flush()

    if type is "GOOD":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stderr.write(GREEN + char + RESET)
                sys.stderr.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stderr.write(BGREEN + char + RESET)
                sys.stderr.flush()

    if type is "VERYBAD":
        if not bold:
            for char in msg:
                sleep(speed)
                sys.stderr.write(RED2 + char + RESET)
                sys.stderr.flush()
        else:         
            for char in msg:
                sleep(speed)
                sys.stderr.write(BRED2 + char + RESET)
                sys.stderr.flush()

    if type is "IRHUMAN":
        if not bold:
            for char in msg:
                sleep(random.uniform(0.05, 0.4))
                sys.stderr.write(GREEN + char + RESET)
                sys.stderr.flush()
        else:         
            for char in msg:
                sleep(random.uniform(0.05, 0.4))
                sys.stderr.write(BGREEN + char + RESET)
                sys.stderr.flush()