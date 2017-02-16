from sys import argv
from time import sleep
from shutil import get_terminal_size


def print_world(world, sizex, sizey):
	print('\033[H')  # move to the top
	print('\033[J')  # clear the screen
	for i in range(sizex + 1):
		for j in range(sizey + 1):
			print("X" if (i, j) in world else "-", end=" ")
		print()


def get_neighbors(cell):
	row, col = cell
	# clockwise
	return set([
		(row - 1, col - 1),
		(row - 1, col),
		(row - 1, col + 1),
		(row, col + 1),
		(row + 1, col + 1),
		(row + 1, col),
		(row + 1, col - 1),
		(row, col - 1)
	])


def evolve(world):
	new_world = set()
	for cell in world:
		neighbors = get_neighbors(cell) 
		if len(world & neighbors) in (2, 3):
			new_world.add(cell)
			
		for cell in neighbors:
			if len(world & set(get_neighbors(cell))) == 3:
				new_world.add(cell)
	return new_world

if __name__ == "__main__":
	world = set()
	with open(argv[1]) as f:
		for row_i, row in enumerate(f):
			for col_i, cell in enumerate(row.split()):
				if cell == "X":
					world.add((row_i, col_i))
	generations = 0
	delay = 0.1
	while True:
		sizey, sizex = get_terminal_size((50, 50))
		sizey = (sizey // 2) - 1
		sizex -= 5
		print_world(world, sizex, sizey)
		info = generations, len(world), delay
		print("generations: {}, population: {}, delay: {} seconds".format(*info))
		print("world size: ", sizey, sizex)
		generations += 1
		world = evolve(world)
		sleep(delay)
