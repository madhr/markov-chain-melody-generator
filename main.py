from mido import MidiFile
from main.sequence_generator import SequenceGenerator
import os.path
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Pass path to midi file')
	parser.add_argument('filename', help="path to midi file")
	args = parser.parse_args()

	file_path = args.filename
	print("getting midi from: ", file_path)
	midi_file = MidiFile(file_path)

	sequence_generator = SequenceGenerator()
	sequence_generator.generate_separate_tracks_from_midi_file(midi_file)

