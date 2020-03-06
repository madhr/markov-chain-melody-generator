import random
import time
from pathlib import Path
from mido import MidiTrack, Message, MidiFile


class Converter:

	DRUMS_CHANNEL = 0

	def parse_track_to_chords(self, track: MidiTrack) -> list:

		track_msgs = self.__filter_out_redundant_track_messages(track)

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

	def __filter_out_redundant_track_messages(self, track):
		filtered = []
		for i, msg in enumerate(track):
			if msg.type == "note_on" and msg.channel != self.DRUMS_CHANNEL:
				filtered.append(msg)
		return filtered

	def parse_chords_to_track(self, chords_list: list, channel, program, velocity, time) -> MidiTrack:
		track = MidiTrack()
		track.append(Message('program_change', channel=channel, program=program, time=0))

		for chord in chords_list:
			for i, note in enumerate(chord):
				note_time = time if i == 0 else 0
				track.append(Message('note_on', note=note, channel=channel, velocity=velocity, time=note_time))
			for i, note in enumerate(chord):
				note_time = time if i == 0 else 0
				track.append(Message('note_off', note=note, channel=channel, velocity=velocity, time=note_time))
		return track

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
		chords = self.parse_track_to_chords(input_track)

		if not chords:
			return None

		self.sort_elements_in_list_of_lists(chords)

		my_dict = self.group_list_elements_into_pairs(chords)

		seed = list(my_dict.keys())[0]

		sequence = self.generate_sequence(my_dict, seed, [], 0, sequence_steps)

		generated_track = self.parse_chords_to_track(sequence, channel, program, velocity, time)

		return generated_track

	def generate_separate_tracks_from_midi_file(self, midi_file: MidiFile):
		generated_tracks = []

		for track in midi_file.tracks:
			generated_track = self.generate_track(track)
			if generated_track:
				generated_tracks.append(generated_track)

		for generated_track in generated_tracks:
			outfile = MidiFile(ticks_per_beat=600)
			outfile.tracks.append(generated_track)
			file_dir = "results"
			Path(file_dir).mkdir(exist_ok=True)
			file_path = file_dir + '/' + str(round(time.time() * 1000)) + '.mid'
			outfile.save(file_path)
			print("saved as ", file_path)

