import sys, pygame
from board import *

# Текущий холст
surface = None

# Текущее игровое поле
board = None

# Выделенная пользователем фигура
selected_figure = None

# Список доступных ходов
avl_moves = []

# Выбранный ход
selected_move = None

# Равен True, если король текущего игрока находится под шахом
shah_flag = False

# Сообщение
msg = None

# Текущий игрок (WHITE или BLACK)
current_player = WHITE


def start():
    global surface, board, selected_figure, avl_moves, selected_move, mode, shah_flag, msg, current_player
    pygame.init()
    pygame.display.set_caption('PyChess')
    surface = pygame.display.set_mode((CELL_SIZE * 8, CELL_SIZE * 8))
    clock = pygame.time.Clock()

    # Создаем игровое поле
    main_board = Board(WHITE)  # WHITE для инициализации, не фиксирует сторону игрока
    board = main_board
    mode = 'mode_1'  # Начинаем с выбора фигуры

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue

                # Режим 1: выбор фигуры текущего игрока
                if mode == 'mode_1':
                    selected_figure = get_mouse_selected_figure(event, current_player)
                    if selected_figure is not None:
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                        if avl_moves:
                            mode = 'mode_2'
                            continue

                # Режим 2: выбор хода или другой фигуры
                if mode == 'mode_2':
                    selected_row, selected_col = get_mouse_selected_cell(event)
                    selected_move = None
                    for move in avl_moves:
                        if selected_row == move.new_row and selected_col == move.new_col:
                            selected_move = move
                            break

                    if selected_move is not None:
                        if selected_move.m_type == CONVERSION:
                            selected_figure = None
                            avl_moves = []
                            board = SelectorBoard(current_player, main_board)
                            mode = 'mode_3'
                            continue
                        mode = 'mode_4'
                        continue

                    new_selected_figure = get_mouse_selected_figure(event, current_player)
                    if new_selected_figure is not None:
                        selected_figure = new_selected_figure
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                    continue

                # Режим 3: выбор фигуры для конверсии
                if mode == 'mode_3':
                    selected_figure = get_mouse_selected_figure(event, current_player)
                    if selected_figure is not None:
                        selected_figure.set_pos(selected_move.new_row, selected_move.new_col)
                        selected_move.new_figure = selected_figure
                        board = main_board
                        mode = 'mode_4'
                        continue

                # Режим 5: игра завершена
                if mode == 'mode_5':
                    pygame.quit()
                    sys.exit()

        # Режим 4: применение хода и смена игрока
        if mode == 'mode_4':
            board.apply_move(selected_move)
            selected_figure = None
            selected_move = None
            avl_moves = []

            shah_flag = False

            game_over = check_game_over(OPPOSITE_SIDE[current_player])
            if game_over == MAT:
                msg = f'Победил {"Белый" if current_player == WHITE else "Черный"}!'
                mode = 'mode_5'
                continue
            if game_over == PAT:
                msg = 'Ничья'
                mode = 'mode_5'
                continue

            current_player = OPPOSITE_SIDE[current_player]
            if board.is_strike_figure(board.kings_dict[current_player]):
                shah_flag = True

            mode = 'mode_1'
            repaint()

        repaint()
        clock.tick(FPS)


def check_game_over(side):
    king = board.kings_dict[side]
    sh_flag = board.is_strike_figure(king)
    avl_flag = (len(board.get_all_avl_moves(side)) == 0)
    if avl_flag and sh_flag:
        return MAT
    if avl_flag and not sh_flag:
        return PAT
    return None


def repaint():
    draw_cells()
    draw_select_cell()
    draw_avl_moves()
    draw_shah_cell()
    draw_figures()
    draw_msg()
    pygame.display.update()


def draw_cells():
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_figures():
    for row in range(0, 8):
        for col in range(0, 8):
            figure = board.get_figure(row, col)
            if figure is None:
                continue
            surface.blit(figure.image, figure.rect)


def draw_select_cell():
    if selected_figure:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_figure.col * CELL_SIZE, selected_figure.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_avl_moves():
    for move in avl_moves:
        row_move = move.new_row
        col_move = move.new_col
        pygame.draw.rect(surface, AVL_MOVE_CELL_COLOR,
                         (col_move * CELL_SIZE + 4, row_move * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))


def draw_shah_cell():
    if shah_flag:
        row = board.kings_dict[current_player].row
        col = board.kings_dict[current_player].col
        pygame.draw.rect(surface, KING_ON_SHAH_COLOR,
                         (col * CELL_SIZE + 4, row * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))


def draw_msg():
    if not msg:
        return
    font = pygame.font.Font(None, 56)
    msg_surface = font.render(msg, 1, MSG_COLOR)
    x_pos = CELL_SIZE * 4 - msg_surface.get_width() // 2
    y_pos = CELL_SIZE * 4 - msg_surface.get_height() // 2
    msg_rect = msg_surface.get_rect(topleft=(x_pos, y_pos))
    surface.blit(msg_surface, msg_rect)


def get_mouse_selected_cell(mouse_event):
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c


def get_mouse_selected_figure(mouse_event, side=None):
    selected_row, selected_col = get_mouse_selected_cell(mouse_event)
    figure = board.get_figure(selected_row, selected_col)
    if side is not None and figure is not None:
        if figure.side != side:
            return None
    return figure


if __name__ == "__main__":
    start()