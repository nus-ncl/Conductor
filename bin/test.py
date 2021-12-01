import sys
import os
import yaml


class Student(object):
	def __init__(self):
		self.__score = None
		self._score = None
		self.score = 1

	def get_score(self):
		return self.__score

	def set_score(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be an integer!')
		if value < 0 or value > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = value


def yaml_dump_to_activity():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	root_path = os.path.dirname(dir_path)
	activity_directory = f"{root_path}/bin"
	a = [1, 2, 3, 4, 9, 3, 9, 9]
	b = [5, 6, 7, 8]
	a[2] = b
	output = {'file': a, 'activity': b}

	if not os.path.exists(activity_directory):
		print('Not existed!')
	# os.mkdir(activity_directory)
	with open(f"{activity_directory}/test.yml", 'w') as stream:
		yaml.safe_dump(output, stream, default_flow_style=False, explicit_start=True, allow_unicode=True,
		               sort_keys=False)


if __name__ == '__main__':
	a=['string','c']
	b=['string','b']
	for index,value in enumerate(a):
		print(a[index] is b[index])

# print(a)
