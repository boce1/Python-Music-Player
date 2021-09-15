import os

def make_default_path(new_path):
	file = open("utils\\_path_\\default_path.txt", "w")
	file.write(new_path)

file = open("utils\\_path_\\default_path.txt", "r")
path = file.read()

list_of_files = []

for root, dirs, files in os.walk(path):
	for file in files:
		if '.mp3' in file:
			list_of_files.append(file)
