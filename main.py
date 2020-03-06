from mido import MidiFile
import datetime
from pathlib import Path
from main.converter import Converter

if __name__ == '__main__':
	mid = MidiFile('resources/AutumnLeaves.mid')

	track_list = mid.tracks
	track = track_list[3]

	converter = Converter()

	generated_track = converter.generate_track(track)

	outfile = MidiFile()
	outfile.ticks_per_beat = 1200

	outfile.tracks.append(generated_track)

	file_dir = "results/"
	file_name = str(datetime.datetime.now())
	Path(file_dir).mkdir(exist_ok=True)
	file_path = file_dir + '/' + file_name + '.mid'
	outfile.save(file_path)

