from mido import MidiTrack

from main.chord import Chord
from main.possibility import Possibility


class Converter:

	def filter_note_on_and_not_drums(self, track):
		filtered = []
		for i, msg in enumerate(track):
			if msg.type == "note_on" and msg.channel != 9:
				filtered.append(msg)
		return filtered

	def get_lowest_note(self, track_msgs) -> int:
		lowest = 110
		for msg in track_msgs:
			if msg.note < lowest:
				lowest = msg.note
		return lowest

	def extract_chords(self, track_msgs):
		outer_list = []
		list = []
		for i, msg in enumerate(track_msgs):
			if i + 1 == len(track_msgs):
				list.append(msg.note)
				outer_list.append(list)
			elif track_msgs[i].time == 0 and track_msgs[i + 1].time > 0:
				list.append(msg.note)
				outer_list.append(list)
				list = []
			elif track_msgs[i].time > 0 and track_msgs[i + 1].time > 0:
				outer_list.append([msg.note])
			else:
				list.append(msg.note)

		return outer_list

	def list_of_lists_to_list_of_chords(self, list_of_lists):
		list_of_chords = []
		for element in list_of_lists:
			chord = Chord(tuple(element))
			list_of_chords.append(chord)

		return list_of_chords

	def add_to_all_elements_in_list_of_lists(self, list_of_lists: list, add: int) -> list:
		for i in range(len(list_of_lists)):
			list_of_lists[i] = [x + add for x in list_of_lists[i]]
		return list_of_lists


	def sort_elements_in_list_of_lists(self, list_of_lists: list) -> list:
		return [sorted(inner) for inner in list_of_lists]

	def group_into_pairs(self, input_list):
		d = dict()
		for i, element in enumerate(input_list):
			if i + 1 != len(input_list):
				d.setdefault(tuple(element), []).append(tuple(input_list[i + 1]))
		return d

	def dict_to_list_of_chords(self, dictionary: dict):
		result = []
		for key, values in dictionary.items():
			chord = Chord(key)
			for val in values:
				possibility = Possibility(Chord(val), values.count(val))
				chord.possibilities.add(possibility)

			for possibility in chord.possibilities:
				all_oocurs_sum = sum([x.no_of_occurs for x in chord.possibilities])
				possibility.normalized_prob = possibility.no_of_occurs * (1/all_oocurs_sum)

			result.append(chord)

		return result

