from unittest import TestCase

from main.sequence_generator import SequenceGenerator


class TestSequenceGenerator(TestCase):

	sequence_generator = SequenceGenerator()

	def test_sort_elements_in_list_of_lists(self):
		list_of_lists = [[8, 4, 6, 1], [3, 9, 1, 7], [3, 6, 4], [1], []]
		goal_list = [[1, 4, 6, 8], [1, 3, 7, 9], [3, 4, 6], [1], []]
		actual_list = self.sequence_generator.sort_elements_in_list_of_lists(list_of_lists)

		self.assertEqual(goal_list, actual_list)

	def test_group_list_chars_into_pairs(self):
		list_of_lists = ['a', 'b', 'a', 'b', 'c', 'd', 'e', 'f', 'c', 'd', 'a', 'e']
		goal_dictionary = {
			('a',): [('b',), ('b',), ('e',)],
			('b',): [('a',), ('c',)],
			('c',): [('d',), ('d',)],
			('d',): [('e',), ('a',)],
			('e',): [('f',)],
			('f',): [('c',)]
		}
		actual_dictionary = self.sequence_generator.group_list_elements_into_pairs(list_of_lists)

		self.assertEqual(goal_dictionary, actual_dictionary)

	def test_group_list_tuples_into_pairs(self):
		list_of_lists = [(1, 5), (5, 7), (7, 8), (1, 5), (5, 7)]
		goal_dictionary = {
			(1, 5): [(5, 7), (5, 7)],
			(5, 7): [(7, 8)],
			(7, 8): [(1, 5)]
		}
		actual_dictionary = self.sequence_generator.group_list_elements_into_pairs(list_of_lists)

		self.assertEqual(goal_dictionary, actual_dictionary)

	def test_generate_sequence(self):
		input_dict = {
			(1, 2):
				[(1, 2), (9,), (1, 2), (9,), (4, 5)],
			(9,):
				[(9,), (9,), (7,), (3, 7)],
			(1, 2, 3):
				[(1, 2, 3), (1, 2, 3), (1, 2, 3), (4, 5)],
			(7,):
				[(7,), (18, 21), (7,), (1, 2, 3)],
			(3, 7):
				[(1, 2)],
			(4, 5):
				[(1, 2, 3), (1, 2, 3)],
			(18, 21):
				[(4, 5), (9,)]
		}
		seed = list(input_dict.keys())[0]

		sequence = self.sequence_generator.generate_sequence(input_dict, seed, [], 0, 10)

		self.assertEqual(10, len(sequence))

