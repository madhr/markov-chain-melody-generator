from mido import MidiFile

from main.converter import Converter

if __name__ == '__main__':
	mid = MidiFile('resources/AutumnLeaves.mid')

	track_list = mid.tracks
	track = track_list[3]

	converter = Converter()
	new_track = converter.filter_note_on_and_not_drums(track)

	lowest_note = converter.get_lowest_note(new_track)
	print("lowest_note", lowest_note)

	chords = converter.extract_chords(new_track)
	print(chords)

	substract_by = (lowest_note * (-1))
	chords_normalized = converter.add_to_all_elements_in_list_of_lists(chords, substract_by)
	print(list(chords_normalized))

	converter.sort_elements_in_list_of_lists(chords_normalized)


