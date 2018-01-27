from copy import deepcopy


class RelativeData:

	def __init__(self, reference_id=0):
		self.reference_id = reference_id
		self.data = {}
		self.data_size = 4

	def relative_to_global(self, id):
		return (id - self.reference_id) % self.data_size

	def global_to_relative(self, id):
		return (id + self.reference_id) % self.data_size

	def make_copy(self, reference_id=None):
		copy = deepcopy(self)
		if reference_id is not None:
			copy.reference_id = reference_id
		return copy

	def __getitem__(self, i):
		if not isinstance(i, int):
			raise ValueError("Expected int, got " + str(type(i)))
		global_id = self.relative_to_global(i)
		return self.data[global_id]

	def __contains__(self, i):
		if not isinstance(i, int):
			raise ValueError("Expected int, got " + str(type(i)))
		global_id = self.relative_to_global(i)
		return global_id in self.data

	def __len__(self):
		return len(self.data)