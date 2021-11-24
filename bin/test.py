import sys
import os

class Student(object):
	def __init__(self):
		self.__score=None
		self._score=None
		self.score=1

	def get_score(self):
		return self.__score

	def set_score(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be an integer!')
		if value < 0 or value > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = value

if __name__ == '__main__':
	# print(sys.path)
	# print('Python %s on %s' % (sys.version, sys.platform))
	# print(default.DEFAULT_VM_OS)
	print(os.environ['PYTHONPATH'])
	print('--')
	print(sys.path)
