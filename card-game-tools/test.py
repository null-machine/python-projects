# def f(sequence=[]):
# 	sequence.append('wtf')
# 	print(sequence)

# f()
# f()
import json

class TestClass:
	def __init__(self, test_dict):
		self.test_dict = test_dict
	
	def __eq__(self, other):
		return self.test_dict == other.test_dict
	
	def __hash__(self):
		# return hash(frozenset(self.test_dict.items()))

test_a = TestClass({'a':1, 'b':1})
test_b = TestClass({'b':1, 'a':1})

print(test_a == test_b)

test_obj_dict = {}
test_obj_dict[test_a] = 2

print(test_b in test_obj_dict)
