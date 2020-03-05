class Chord:

	def __init__(self, notes: tuple):
		self.notes = notes
		self.possibilities = set()

	def __eq__(self, o: object) -> bool:
		return self.notes == o.notes




