import random
import time
import copy
import os
from pprint import pprint
import keyboard


def get_generated_maze(size = 15):
    columns, rows = size, size
    maze = [[1 for _ in range(columns)] for _ in range(rows)]
    maze[-3][0] = 0  # Вход
    maze[2][-1] = 0  # Выход

    stack = [(random.randrange(1, rows, 2), random.randrange(1, columns, 2))]

    while stack:
        row, column = stack[-1]
        maze[row][column] = 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        found = False

        for x, y in directions:
            new_row, new_column = row + 2 * x, column + 2 * y

            if (
                0 <= new_row < rows
                and 0 <= new_column < columns
                and maze[new_row][new_column] == 1
            ):
                maze[row + x][column + y] = 0
                stack.append((new_row, new_column))
                found = True
                break

        if not found:
            stack.pop()

    # Чтобы никогда не было закрытого входа и выхода
    maze[-3][1] = 0  # Вход
    maze[2][-2] = 0  # Выход

    return maze


def fill_maze_with_coins(maze: list, chance: float = 0.2):
    chance = 1 - chance

    for i, row in enumerate(maze):
        for j, column in enumerate(row):
            if column == 0 and random.random() > chance:
                maze[i][j] = 3
    return maze


def print_maze(maze: list):
    objects = ["  ", "██", "☻ ", "• "]
    for i in maze:
        for j in i:
            print(objects[j], end="")
        print()


def check_coin(maze: list, maze_size: int, player_position: list):
    for i in range(maze_size):
        for j in range(maze_size):
            if maze[i][j] == 3 and player_position == [i, j]:
                return True
    return False


def movement(maze: list, player_position: list, maze_size: int):
    coins = 0
    while True:

        copied_maze = copy.deepcopy(maze)
        copied_maze[player_position[0]][player_position[1]] = 2
        os.system("cls")
        print_maze(copied_maze)

        key_pressed = keyboard.read_event(True)
        if key_pressed.event_type == keyboard.KEY_DOWN:
            if key_pressed.name == "a" and player_position[1] > 0:
                player_position[1] -= 1
            elif key_pressed.name == "d" and player_position[1] < maze_size-1:
                player_position[1] += 1
            elif key_pressed.name == "w" and player_position[0] > 0:
                player_position[0] -= 1
            elif key_pressed.name == "s" and player_position[0] < maze_size-1:
                player_position[0] += 1
            elif key_pressed.name == "e":
                exit(0)
            
            if check_coin(maze, maze_size, player_position):
                maze[player_position[0]][player_position[1]] = 0
                coins += 1

            


def main():
    SIZE = 15
    generated_maze = get_generated_maze(SIZE)
    fill_maze_with_coins(generated_maze, chance=0.1)
    maze = copy.deepcopy(generated_maze)
    player_position = [SIZE-3, 0]

    movement(maze, player_position, SIZE)


if __name__ == "__main__":
    main()
