from unittest import TestCase

from main.midi_parser import MidiParser
from mido import Message, MidiTrack


class TestMidiParser(TestCase):
	midi_parser = MidiParser()

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
		actual_chords = self.midi_parser.parse_track_to_chords(track)

		self.assertEqual(goal_chords, actual_chords)


	def test_parse_chords_to_track_equals_messages_size(self):

		chords_list = [(1, 2), (3, 4, 5)]

		# count all notes for 'note_on' and 'note_off' (*2) and 'program_change' (+1)
		goal_track_len = sum(len(note) for note in chords_list) * 2 + 1
		actual_track = self.midi_parser.parse_chords_to_track(chords_list, channel=1, program=10, velocity=60, time=30)

		self.assertEqual(goal_track_len, len(actual_track))

