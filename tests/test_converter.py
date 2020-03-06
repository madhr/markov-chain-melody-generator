from unittest import TestCase
from mido import Message, MidiTrack

from main.converter import Converter


class TestConverter(TestCase):
	converter = Converter()

	def test_parse_track_to_chords(self):
		msg1 = Message(type="note_on", channel=1, note=60, time=100)
		msg2 = Message(type="note_on", channel=1, note=61, time=0)
		msg3 = Message(type="note_on", channel=1, note=62, time=0)
		msg4 = Message(type="note_on", channel=1, note=63, time=50)
		msg5 = Message(type="note_on", channel=1, note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]
		track = MidiTrack()
		for msg in msg_list:
			track.append(msg)

		goal_chords = [[60, 61, 62], [63, 64]]
		actual_chords = self.converter.parse_track_to_chords(track)

		self.assertEqual(goal_chords, actual_chords)

	def test_sort_elements_in_list_of_lists(self):
		list_of_lists = [[8, 4, 6, 1], [3, 9, 1, 7], [3, 6, 4], [1], []]
		goal_list = [[1, 4, 6, 8], [1, 3, 7, 9], [3, 4, 6], [1], []]
		actual_list = self.converter.sort_elements_in_list_of_lists(list_of_lists)

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
		actual_dictionary = self.converter.group_list_elements_into_pairs(list_of_lists)

		self.assertEqual(goal_dictionary, actual_dictionary)

	def test_group_list_tuples_into_pairs(self):
		list_of_lists = [(1, 5), (5, 7), (7, 8), (1, 5), (5, 7)]
		goal_dictionary = {
			(1, 5): [(5, 7), (5, 7)],
			(5, 7): [(7, 8)],
			(7, 8): [(1, 5)]
		}
		actual_dictionary = self.converter.group_list_elements_into_pairs(list_of_lists)

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

		sequence = self.converter.generate_sequence(input_dict, seed, [], 0, 10)

		self.assertEqual(10, len(sequence))

