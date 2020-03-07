import random
from mido import MidiTrack, MidiFile

from main.midi_parser import MidiParser


class SequenceGenerator:

	def sort_elements_in_list_of_lists(self, list_of_lists: list) -> list:
		return [sorted(inner) for inner in list_of_lists]

	def group_list_elements_into_pairs(self, input_list):
		d = dict()
		for i, element in enumerate(input_list):
			if i + 1 != len(input_list):
				d.setdefault(tuple(element), []).append(tuple(input_list[i + 1]))
		return d

	def generate_sequence(self, input_dict, current, sequence, count, max):
		if max == count:
			return sequence
		candidates = input_dict[current]

		occurs_dict = dict()
		probabilities_list = []
		for cand in candidates:
			occurs_dict[cand] = candidates.count(cand)

		all_ocurs_sum = sum(occurs_dict.values())

		for key in occurs_dict:
			normalized_prob = occurs_dict[key] * (1 / all_ocurs_sum)
			probabilities_list.append(normalized_prob)

		opts_list = list(occurs_dict.keys())

		chosen = random.choices(opts_list, probabilities_list)[0]
		sequence.append(chosen)
		count = count+1
		return self.generate_sequence(input_dict, chosen, sequence, count, max)

	def generate_track(self, input_track: MidiTrack, sequence_steps=100, channel=0, program=12, velocity=60, time=300) -> MidiTrack:
		midi_parser = MidiParser()
		chords = midi_parser.parse_track_to_chords(input_track)
		if not chords: return None

		self.sort_elements_in_list_of_lists(chords)
		my_dict = self.group_list_elements_into_pairs(chords)
		seed = list(my_dict.keys())[0]
		sequence = self.generate_sequence(my_dict, seed, [], 0, sequence_steps)
		return midi_parser.parse_chords_to_track(sequence, channel, program, velocity, time)

	def generate_separate_tracks_from_midi_file(self, midi_file: MidiFile):
		midi_parser = MidiParser()
		generated_tracks = []

		for track in midi_file.tracks:
			generated_track = self.generate_track(track)
			if generated_track:
				generated_tracks.append(generated_track)
		midi_parser.save_tracks_to_file(generated_tracks)

