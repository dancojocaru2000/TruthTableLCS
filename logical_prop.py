# ! = Negate
# &, ^ = And, Conjunction
# |, v = Or, Disjunction
# > = Implies
# = = Equivalence
# Capital letter = atom

def negate(val):
	return not val

def conj(val1, val2):
	return val1 and val2

def disj(val1, val2):
	return val1 or val2

def impl(val1, val2):
	return not (val1 and not val2)

def equiv(val1, val2):
	return val1 == val2

def is_two_param_operator(op):
	return op in ['&', '|', '>', '=']

def is_atom(elem):
	if type(elem) != type(""):
		return False
	return elem.isupper()

def is_atom_or_list(elem):
	if type(elem) == type([]):
		return True
	else:
		return is_atom(elem)

def op_to_str(op):
	if op == '!':
		return '¬'
	if op == '&':
		return '∧'
	if op == "|":
		return '∨'
	if op == '>':
		return '→'
	if op == '=':
		return '≡'

def logic_prop_to_str(prop):
	if is_atom(prop):
		return prop
	if len(prop) == 2:
		return "(" + op_to_str(prop[0]) + "" + logic_prop_to_str(prop[1]) + ")"
	if len(prop) == 3:
		return "(" + logic_prop_to_str(prop[0]) + \
			"" + op_to_str(prop[1]) + "" + logic_prop_to_str(prop[2]) + ")"
	


class LogicProposition:
	def __str__(self):
		return logic_prop_to_str(self.prop)

	def __init__(self, proposition, atoms=None):
		if type(proposition) == type(""):
			proposition = proposition.strip()

			if len(proposition) == 1:
				self.prop = proposition
				self.atoms = set([proposition])
				return

			self.prop = None
			self.atoms = set()

			def create_prop(it):
				element = []
				try:
					while True:
						i = next(it)
						if i == '(':
							element.append(create_prop(it))
						elif i == '!' or i == '¬':
							element.append('!')
						elif i == '&' or i == '^' or i == '∧':
							element.append('&')
						elif i == '|' or i == 'v' or i == 'V' or i == '∨':
							element.append('|')
						elif i == '>' or i == '→':
							element.append('>')
						elif i == '=' or i == '≡':
							element.append('=')
						elif i == ')':
							if len(element) == 2:
								assert(element[0] == '!')
								assert(is_atom_or_list(element[1]))
							elif len(element) == 3:
								assert(is_two_param_operator(element[1]))
								assert(is_atom_or_list(element[0]))
								assert(is_atom_or_list(element[2]))

							return element		# Finished element )
						elif i.isupper() and i.isalpha():
							element.append(i)  # Atom
							self.atoms.add(i)
						elif i == ' ':
							pass
						else:
							raise ValueError(f"Unexpected value: {i}")
				except StopIteration:
					raise StopIteration
					# return element

			it = iter(proposition)
			assert(next(it) == '(')
			self.prop = create_prop(iter(it))
		else:
			self.prop = proposition
			self.atoms = atoms
			if self.atoms is None:
				self.atoms = set()
				def gen_atoms(prop):
					if is_atom(prop):
						self.atoms.add(prop)
					elif len(prop) == 2:
						gen_atoms(prop[1])
					elif len(prop) == 3:
						gen_atoms(prop[0])
						gen_atoms(prop[2])
				gen_atoms(self.prop)

		self.atoms = list(sorted(list(self.atoms)))


	def all_combinations(self):
		limit = len(self.atoms)

		def gen(val=0, l=[]):
			if val == limit:
				yield l
			else:
				yield from gen(val + 1, l + [False])
				yield from gen(val + 1, l + [True])

		return gen()

	def evaluate(self, values):
		def ev(elem):
			if is_atom(elem):
				return values[elem]
			if len(elem) == 2:
				return negate(ev(elem[1]))
			elif len(elem) == 3:
				if elem[1] == '&':
					return conj(ev(elem[0]), ev(elem[2]))
				elif(elem[1] == '|'):
					return disj(ev(elem[0]), ev(elem[2]))
				elif(elem[1] == '>'):
					return impl(ev(elem[0]), ev(elem[2]))
				elif(elem[1] == '='):
					return equiv(ev(elem[0]), ev(elem[2]))

		return ev(self.prop)

	def all_subpropositions(self):
		def gen(prop):
			if is_atom(prop):
				return
			if len(prop) == 2:
				yield from gen(prop[1])
			elif len(prop) == 3:
				yield from gen(prop[0])
				yield from gen(prop[2])

			yield LogicProposition(prop, self.atoms)
		return gen(self.prop)

# LP = LogicProposition
# l = LP("((P > Q) > ((Q > S) > ((P v Q) > R)))")
# # print(l)
# # print(l.atoms)
# # for i in l.all_combinations():
# # 	values = {}

# # 	for j in zip(l.atoms, i):
# # 		values[j[0]] = j[1]

# # 	print({k:"T" if v else "F" for k, v in values.items()})
# # 	print("T" if l.evaluate(values) else "F")
# # 	print()

def print_table(table, max_width, print_color=False):
	def color(c, s):
		esc = chr(27)
		return esc + "[" + str(c) + "m" + str(s) + esc + "[0m"

	if max_width is None:
		max_width = [10] * len(table[0])
	for line in table:
		for i, item in zip(range(100000), line):
			if print_color and item == 'T':
				print(color(92, str(item).rjust(max_width[i])), end=" | ")
			elif print_color and item == 'F':
				print(color(91, str(item).rjust(max_width[i])), end=" | ")
			else:
				print(str(item).rjust(max_width[i]), end=" | ")
		print()

def gen_table(prop):
	table = []

	def first_line():
		line = []
		line.append('#')
		line += list(prop.atoms)
		# line.append(l)
		line += list(prop.all_subpropositions())
		return line
	table.append(first_line())

	for no, i in zip(range(99999), prop.all_combinations()):
		line = []
		line.append(no + 1)
		line += ["T" if elem else "F" for elem in i]
		# line.append(
		# 	l.evaluate(
		# 		{j[0]: j[1] for j in zip(l.atoms, i)}
		# 	)
		# )
		for prop in prop.all_subpropositions():
			value = prop.evaluate(
				{j[0]: j[1] for j in zip(prop.atoms, i)}
			)
			line.append("T" if value else "F")
		table.append(line)

	return table

def get_max_width(table):
	width = [0] * len(table[0])
	for line in table:
		for i in range(len(line)):
			new_width = len(str(line[i]))
			if width[i] < new_width:
				width[i] = new_width
	return width

# table = gen_table()
# print_table(table, get_max_width(table))

# # for prop in l.all_subpropositions():
# # 	print(prop)