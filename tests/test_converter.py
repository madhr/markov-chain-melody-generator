from unittest import TestCase
from mido import Message

from main.chord import Chord
from main.converter import Converter


class TestConverter(TestCase):
	converter = Converter()

	def test_filter_note_on_and_not_drums(self):
		msg1 = Message(type="note_on", channel=9, note=60, time=100)
		msg2 = Message(type="note_off", channel=2, note=61, time=0)
		msg3 = Message(type="note_on", channel=2, note=62, time=0)
		msg4 = Message(type="note_off", channel=2, note=63, time=50)
		msg5 = Message(type="note_on", channel=2, note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		goal_msg = [msg3, msg5]
		actual_msg = self.converter.filter_note_on_and_not_drums(msg_list)

		self.assertEqual(goal_msg, actual_msg)

	def test_get_lowest_note(self):
		msg1 = Message(type="note_on", note=60, time=100)
		msg2 = Message(type="note_on", note=61, time=0)
		msg3 = Message(type="note_on", note=62, time=0)
		msg4 = Message(type="note_on", note=63, time=50)
		msg5 = Message(type="note_on", note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		goal_lowest = 60
		actual_lowest = self.converter.get_lowest_note(msg_list)

		self.assertEqual(goal_lowest, actual_lowest)

	def test_extract_chords(self):
		msg1 = Message(type="note_on", note=60, time=100)
		msg2 = Message(type="note_on", note=61, time=0)
		msg3 = Message(type="note_on", note=62, time=0)
		msg4 = Message(type="note_on", note=63, time=50)
		msg5 = Message(type="note_on", note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		goal_chords = [[60, 61, 62], [63, 64]]
		actual_chords = self.converter.extract_chords(msg_list)

		self.assertEqual(goal_chords, actual_chords)

	def test_add_to_all_elements_in_list_of_lists(self):
		list_of_lists = [[3, 8], [5, 10], [], [0], [2, 7, 7, 3]]
		increase_by = 5
		goal_list = [[8, 13], [10, 15], [], [5], [7, 12, 12, 8]]
		actual_list = self.converter.add_to_all_elements_in_list_of_lists(list_of_lists, increase_by)

		self.assertEqual(goal_list, actual_list)

	def test_sort_elements_in_list_of_lists(self):
		list_of_lists = [[8, 4, 6, 1], [3, 9, 1, 7], [3, 6, 4], [1], []]
		goal_list = [[1, 4, 6, 8], [1, 3, 7, 9], [3, 4, 6], [1], []]
		actual_list = self.converter.sort_elements_in_list_of_lists(list_of_lists)

		self.assertEqual(goal_list, actual_list)

	def test_group_into_pairs(self):
		list_of_lists = ['a', 'b', 'a', 'b', 'c', 'd', 'e', 'f', 'c', 'd', 'a', 'e']
		goal_dictionary = {
			('a',): [('b',), ('b',), ('e',)],
			('b',): [('a',), ('c',)],
			('c',): [('d',), ('d',)],
			('d',): [('e',), ('a',)],
			('e',): [('f',)],
			('f',): [('c',)]
		}
		actual_dictionary = self.converter.group_into_pairs(list_of_lists)

		self.assertEqual(goal_dictionary, actual_dictionary)

	def test_group_chords_into_pairs(self):
		list_of_lists = [Chord((1, 5)).notes, Chord((5, 7)).notes, Chord((7, 8)).notes, Chord((1, 5)).notes,
						 Chord((5, 7)).notes]
		goal_dictionary = {
			(1, 5): [(5, 7), (5, 7)],
			(5, 7): [(7, 8)],
			(7, 8): [(1, 5)]
		}
		actual_dictionary = self.converter.group_into_pairs(list_of_lists)

		self.assertEqual(goal_dictionary, actual_dictionary)

	def test_list_of_lists_to_list_of_chords(self):
		list_of_lists = [[8, 4, 6, 1], [6]]

		goal_list_of_chords = [(8, 4, 6, 1), (6,)]
		actual_list_of_chords = self.converter.list_of_lists_to_list_of_chords(list_of_lists)

		self.assertEqual(goal_list_of_chords[0], actual_list_of_chords[0].notes)
		self.assertEqual(goal_list_of_chords[1], actual_list_of_chords[1].notes)

	def test_dict_to_list_of_chords_possibilities_sum_to_one(self):
		dictionary = {
			(1, 2):
				[(1, 2), (9,), (1, 2), (9,), (5, 7)],
			(9,):
				[(9,), (9,), (1, 6), (3, 7)],
			(1, 2, 3):
				[(1, 2, 3), (1, 2, 3), (1, 2, 3), (4, 5)],
			(7,):
				[(7,), (18, 21), (7,), (18, 33)]
		}

		actual_list_of_chords = self.converter.dict_to_list_of_chords(dictionary)
		for chord in actual_list_of_chords:
			self.assertAlmostEqual(1.0, sum([pos.normalized_prob for pos in chord.possibilities]))

