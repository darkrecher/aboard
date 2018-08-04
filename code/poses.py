# -*- coding: UTF-8 -*-


class Poses:

	def __init__(self):
		self.poses = [1, 2, 5, 8, 90, 91, 92]

	def pouet(
		self, sense='┌ ┐ └ ┘', tell_prime_coord_change=False,
		skip_lines=None, rect=None, poses=None,
		sliding_window=None, continuous_sliding_window=None
	):
		pass

	def __iter__(self):
		return self

	def __next__(self):

		if not self.poses:
			raise StopIteration

		return self.poses.pop(0)

	def skip(self):

		if self.poses:
			self.poses.pop(0)


# ----------------- tests des trucs en cours ------------------

def main():

	p = Poses()

	for elem in p:
		print(elem)

	print('-' * 20)

	p2 = Poses()

	for elem in p2:
		if elem in (2, 91):
			p2.skip()
			p2.skip()
		print(elem)


if __name__ == '__main__':
	main()
