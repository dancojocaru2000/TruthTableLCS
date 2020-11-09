from logical_prop import LogicProposition, gen_table, get_max_width, print_table

print(" ! is the symbol for not\n","| is the symbol for or\n","& is the symbol for and\n","> is the symbol for implies\n","= is the symbol for if and only if\n","Any upper case letter is an atomic proposition")
p = input(" Plese input a string of symbols:\n")

prop = LogicProposition(p)

table = gen_table(prop)
print_table(table, get_max_width(table))