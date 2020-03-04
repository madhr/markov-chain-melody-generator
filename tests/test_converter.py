from unittest import TestCase
from mido import Message

from main.converter import Converter


class TestConverter(TestCase):

	converter = Converter()

	def test_filter_note_on_and_not_drums(self):
		msg1 = Message(type="note_on", channel=9, note=60, time=100)
		msg2 = Message(type="note_off", channel=2, note=61, time=0)
		msg3 = Message(type="note_on", channel=2,note=62, time=0)
		msg4 = Message(type="note_off", channel=2, note=63, time=50)
		msg5 = Message(type="note_on", channel=2, note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		msg_expected = [msg3, msg5]
		msg_actual = self.converter.filter_note_on_and_not_drums(msg_list)

		self.assertEqual(msg_expected, msg_actual)

	def test_get_lowest_note(self):
		msg1 = Message(type="note_on", note=60, time=100)
		msg2 = Message(type="note_on", note=61, time=0)
		msg3 = Message(type="note_on", note=62, time=0)
		msg4 = Message(type="note_on", note=63, time=50)
		msg5 = Message(type="note_on", note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		lowest_expected = 60
		lowest = self.converter.get_lowest_note(msg_list)
		self.assertEqual(lowest_expected, lowest)

	def test_extract_chords(self):
		msg1 = Message(type="note_on", note=60, time=100)
		msg2 = Message(type="note_on", note=61, time=0)
		msg3 = Message(type="note_on", note=62, time=0)
		msg4 = Message(type="note_on", note=63, time=50)
		msg5 = Message(type="note_on", note=64, time=0)
		msg_list = [msg1, msg2, msg3, msg4, msg5]

		goal_chords = [[60, 61, 62], [63, 64]]
		chords = self.converter.extract_chords(msg_list)

		self.assertEqual(goal_chords, chords)

	def test_add_to_all_elements_in_list_of_lists(self):
		list_of_lists = [[3, 8], [5, 10], [], [0], [2, 7, 7, 3]]
		increase_by = 5
		goal_list = [[8, 13], [10, 15], [], [5], [7, 12, 12, 8]]

		increased_list = self.converter.add_to_all_elements_in_list_of_lists(list_of_lists, increase_by)
		self.assertEqual(goal_list, increased_list)

	def test_sort_elements_in_list_of_lists(self):

		list_of_lists = [[8, 4, 6, 1], [3, 9, 1, 7], [3, 6, 4], [1], []]
		goal_list = [[1, 4, 6, 8], [1, 3, 7, 9], [3, 4, 6], [1], []]

		sorted_list = self.converter.sort_elements_in_list_of_lists(list_of_lists)

		self.assertEqual(goal_list, sorted_list)
