#!/usr/bin/env python3

from logical_prop import LogicProposition, gen_table, get_max_width, print_table
from sys import stdout, stdin

p = None
if stdout.isatty() and stdin.isatty():
	print(" ! is the symbol for not\n","| is the symbol for or\n","& is the symbol for and\n","> is the symbol for implies\n","= is the symbol for if and only if\n","Any upper case letter is an atomic proposition")
	p = input(" Please input a string of symbols:\n")
else:
	p = input()

prop = LogicProposition(p)

def should_print_color():
	# Print color only if the output is a terminal
	# If the output is a file, print normally
	if not stdout.isatty():
		return False

	import os

	# Some users prefer to disable colors in output of programs
	# Those users generally set the NO_COLOR environment variable
	# to any value. The program should respect that choice.
	# See: https://no-color.org/
	if os.getenv("NO_COLOR") is not None:
		return False

	return True

table = gen_table(prop)
print_table(table, get_max_width(table), print_color=should_print_color())
