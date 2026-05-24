import cv2
from pathlib import Path
from vision import read_puzzle

def is_valid(board, y,x ,i):
    if i in board[y]:
        return False
    
    column = [board[r][x] for r in range(9)]
    if i in column:
        return False

    start_row = (y//3) * 3
    start_col = (x//3) * 3

    for r in range(start_row, start_row+3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == i:
                return False
    
    return True
def solve_board(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:  # empty cell
                for i in range(1, 10):  # candidates 1–9
                    if is_valid(board, y, x, i):
                        board[y][x] = i
                        if solve_board(board):  # recurse deeper
                            return True
                        board[y][x] = 0  # backtrack
                return False  # no valid number found
    return True  # solved (no empty cells left)


def print_sudoku(board):
    for row in board:
        print(row)

def main():
    img_path = Path(__file__).parent / "img" / "puzzle_2.png"
    print(img_path)
    print(img_path.exists())

    puzzle_img = cv2.imread(str(img_path))
    scanned_board = read_puzzle(puzzle_img)

    print("\nSudoku Board:")
    for row in scanned_board:
        print(row)

    if solve_board(scanned_board):
        print("\nSolved Sudoku Board:")
        print_sudoku(scanned_board)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()