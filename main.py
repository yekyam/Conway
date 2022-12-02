import pygame
import random

GRID_SIZE = 100

MARGIN = 2
WIDTH = 500
HEIGHT = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

def make_grid(size, is_clear=True):
	grid = []
	for x in range(size):
		temp = []
		for y in range(size):
			if is_clear:
				temp.append(0)
			else:
				temp.append(random.randint(0, 1))
		grid.append(temp)
	return grid


def is_valid_pos(grid, row, col):
	grid_size = len(grid)
	return (row >= 0 ) and (row < grid_size) and (col >= 0) and (col < grid_size)


def get_live_neighbors(grid, row, col):
	grid_size = len(grid)
	count = 0

	if is_valid_pos(grid, row, col+1):
		if grid[row][col+1] == 1:
			count+=1

	if is_valid_pos(grid, row, col-1):
		if grid[row][col-1] == 1:
			count+=1

	if is_valid_pos(grid, row-1, col+1):
		if grid[row-1][col+1] == 1:
			count+=1

	if is_valid_pos(grid, row-1, col-1):
		if grid[row-1][col-1] == 1:
			count+=1
	
	if is_valid_pos(grid, row-1, col):
		if grid[row-1][col] == 1:
			count+=1

	if is_valid_pos(grid, row+1, col+1):
		if grid[row+1][col+1] == 1:
			count+=1

	if is_valid_pos(grid, row+1, col-1):
		if grid[row+1][col-1] == 1:
			count+=1
	
	if is_valid_pos(grid, row+1, col):
		if grid[row+1][col] == 1:
			count+=1

	return count

# Any live cell with two or three live neighbours survives.
# Any dead cell with three live neighbours becomes a live cell.
# All other live cells die in the next generation. Similarly, all other dead cells stay dead.

def update(grid):
	new_grid = [x[:] for x in grid]
	grid_size = len(grid)
	for i in range(grid_size):
		for j in range(grid_size):
			num_live_neighbors = get_live_neighbors(grid, i, j)
			if grid[i][j] == 1:
				if not num_live_neighbors in [2, 3]:
					new_grid[i][j] = 0
			else:
				if num_live_neighbors == 3:
					new_grid[i][j] = 1
	return new_grid


def display_grid(grid):
	print('*'*50)
	for row in grid:
		for pos in row:
			piece = ' '
			if pos == 1:
				piece = 'X'
			print(f'|{piece}', end='', sep='')
		print('|')
	print('*'*50)


def display_grid_to_screen(window, grid):
	grid_size = len(grid)
	square_size = WIDTH / grid_size
	for i in range(grid_size):
		for j in range(grid_size):
			rect = pygame.Rect(j * (MARGIN + square_size) + MARGIN, i * (MARGIN + square_size) + MARGIN, square_size, square_size)
			if grid[i][j] == 1:
				color = WHITE
			else:
				color = BLACK
			pygame.draw.rect(window, color, rect)


def calculate_square_clicked(grid, pos: tuple[int, int]):
	square_size = WIDTH / len(grid)
	x, y = pos
	col = x // (square_size + MARGIN)
	row = y // (square_size + MARGIN)
	return int(row), int(col)


def main():
	pygame.init()


	window = pygame.display.set_mode((WIDTH, HEIGHT))
	grid = make_grid(GRID_SIZE)
	is_running = False
	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					grid = make_grid(GRID_SIZE, False)
				if event.key == pygame.K_SPACE:
					is_running = not is_running
				if event.key == pygame.K_c:
					grid = make_grid(GRID_SIZE)
					
			
			if not is_running and event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				
				row, col = calculate_square_clicked(grid, pos)
				grid[row][col] = 0 if grid[row][col] else 1
		
		
		window.fill((GRAY))

		display_grid_to_screen(window, grid)
		if is_running:
			grid = update(grid)
			clock.tick(4)
		else:
			clock.tick(60)
		

		pygame.display.flip()


main()
pygame.quit()