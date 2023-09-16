import os
import time
import copy
import random

import keyboard
from colorama import Fore, Back, Style


def get_generated_maze(size=15):
    columns, rows = size, size
    maze = [[1 for _ in range(columns)] for _ in range(rows)]
    maze[-3][0] = 0  # Вход
    maze[2][-1] = 1  # Выход

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

    # Чтобы никогда не было стенки перед выходом
    maze[-3][1] = 0  # для входа
    maze[2][-2] = 0  # для выхода

    return maze


def fill_maze_with_coins(maze: list, chance: float = 0.2):
    chance = 1 - chance

    for i, row in enumerate(maze):
        for j, column in enumerate(row):
            if column == 0 and random.random() > chance:
                maze[i][j] = 3
    return maze


def print_maze(maze: list):
    objects = ["  ", "██", Fore.LIGHTYELLOW_EX + "☻ ", Fore.LIGHTGREEN_EX + "• "]
    for i in maze:
        for j in i:
            print(objects[j], end="")
            print(Style.RESET_ALL, end="")
        print()


def check_coin(maze: list, player_position: list):
    return maze[player_position[0]][player_position[1]] == 3


def check_area_for_coins(maze: list):
    return any(cell == 3 for row in maze for cell in row)


def get_coins_count(maze: list):
    return sum(row.count(3) for row in maze)


def check_win(player_position: list, maze_size: int):
    return player_position == [2, maze_size - 1]


def check_wall(maze: list, player_position: list):
    return maze[player_position[0]][player_position[1]] == 1


def movement(maze: list, player_position: list, maze_size: int):
    coins = 0
    start_time = time.time()

    while True:
        copied_maze = copy.deepcopy(maze)
        copied_maze[player_position[0]][player_position[1]] = 2

        os.system("cls")
        print(Fore.LIGHTCYAN_EX + f"| {get_coins_count(maze)} coins left")
        print(Style.RESET_ALL, end="")
        print_maze(copied_maze)

        key_pressed = keyboard.read_event(True)

        maze[2][-1] = check_area_for_coins(copied_maze)

        if check_coin(maze, player_position):
            maze[player_position[0]][player_position[1]] = 0
            coins += 1

        if check_win(player_position, maze_size):
            os.system("cls")
            print(Fore.LIGHTGREEN_EX + f"You won! You have played {int(time.time() - start_time)} seconds!")
            print(Style.RESET_ALL)
            exit(0)

        if key_pressed.event_type == keyboard.KEY_DOWN:
            if (
                key_pressed.name == "a"
                and player_position[1] > 0
                and not check_wall(
                    copied_maze, [player_position[0], player_position[1] - 1]
                )
            ):
                player_position[1] -= 1
            elif (
                key_pressed.name == "d"
                and player_position[1] < maze_size - 1
                and not check_wall(
                    copied_maze, [player_position[0], player_position[1] + 1]
                )
            ):
                player_position[1] += 1
            elif (
                key_pressed.name == "w"
                and player_position[0] > 0
                and not check_wall(
                    copied_maze, [player_position[0] - 1, player_position[1]]
                )
            ):
                player_position[0] -= 1
            elif (
                key_pressed.name == "s"
                and player_position[0] < maze_size - 1
                and not check_wall(
                    copied_maze, [player_position[0] + 1, player_position[1]]
                )
            ):
                player_position[0] += 1
            elif key_pressed.name == "e":
                exit(0)


def main():
    SIZE = 15
    generated_maze = get_generated_maze(SIZE)
    fill_maze_with_coins(generated_maze, chance=0.1)
    maze = copy.deepcopy(generated_maze)
    player_position = [SIZE - 3, 0]

    movement(maze, player_position, SIZE)


if __name__ == "__main__":
    main()
