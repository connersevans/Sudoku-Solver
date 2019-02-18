import homework4

while True:

    print('Please enter the filename of the Soduku puzzle you would like solved')
    print('Enter "quit" to end the program')

    x = input()

    x = x.lower()

    if x == 'easy.txt':
        easy_board = homework4.read_board('easy.txt')
        easy_solver = homework4.Sudoku(easy_board)
        easy_solver.infer_ac3()
        easy_solver.create_solution()

    elif x == 'medium1.txt' or x == 'medium2.txt' or x == 'medium3.txt' or x == 'medium4.txt':
        medium_board = homework4.read_board(x)
        medium_solver = homework4.Sudoku(medium_board)
        medium_solver.infer_improved()
        medium_solver.create_solution()

    elif x == 'hard1.txt' or x == 'hard2.txt':
        hard_board = homework4.read_board(x)
        hard_solver = homework4.Sudoku(hard_board)
        hard_solver.infer_with_guessing()
        hard_solver.create_solution()

    elif x == 'quit':
        break

    else:
        print('That was not a valid puzzle')
        continue