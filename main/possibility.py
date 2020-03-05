from main.chord import Chord


class Possibility:

	def __init__(self, chord: Chord, no_of_occurs: int):
		self.chord = chord
		self.no_of_occurs = no_of_occurs
		self.normalized_prob = None

	def __eq__(self, o: object) -> bool:
		return self.chord.notes == o.chord.notes

	def __hash__(self) -> int:
		return hash(self.chord.notes)



