from mido import MidiFile
from main.converter import Converter

if __name__ == '__main__':
	midi_file = MidiFile('resources/TaketheAtrain.mid')

	converter = Converter()
	converter.generate_separate_tracks_from_midi_file(midi_file)

