from mido import MidiTrack, Message, MidiFile
import time
from pathlib import Path

class MidiParser:

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

	def save_tracks_to_file(self, generated_tracks):

		for generated_track in generated_tracks:
			outfile = MidiFile(ticks_per_beat=600)
			outfile.tracks.append(generated_track)
			file_dir = "results"
			Path(file_dir).mkdir(exist_ok=True)
			file_path = file_dir + '/' + str(round(time.time() * 1000)) + '.mid'
			outfile.save(file_path)
			print("new single track file saved at:", file_path)
