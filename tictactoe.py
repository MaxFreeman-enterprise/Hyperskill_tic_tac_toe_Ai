from abc import ABC, abstractmethod
import random
import re
from minimax import Game


class Turn:
    turn_marks = ("X", "O")

    def __init__(self, turn):
        if turn in self.turn_marks:
            self.current_turn = turn
        else:
            self.current_turn = self.turn_marks[0]

    def toggle_turn(self):
        self.current_turn = self.get_next_turn()

    def get_next_turn(self):
        if self.current_turn == self.turn_marks[0]:
            return self.turn_marks[1]

        else:
            return self.turn_marks[0]



class Board:
    def __init__(self, board=None):
        # self.board_array = [list(self.board_string[0:3]), list(self.board_string[3:6]), list(self.board_string[6:9])]
        if board is None:
            self.board_array = [["_", "_", "_"] for _ in range(3)]
            self.board_string = "_________"
        elif isinstance(board, type([[""]])):
            self.board_array = [row[:] for row in board]
            self.board_string = self.make_board_string()
        elif isinstance(board, Board):
            self.board_array = [row[:] for row in board.board_array]
            self.board_string = self.make_board_string()

    def make_pretty_board(self) -> str:
        b = self.board_string.replace("_", " ")
        return f"""    ---------
    | {b[0]} {b[1]} {b[2]} |
    | {b[3]} {b[4]} {b[5]} |
    | {b[6]} {b[7]} {b[8]} |
    ---------"""

    #  TODO: make enum for game states
    def get_game_state(self) -> str:
        board = self.board_string
        if re.search("XXX......", board) or re.search("...XXX...", board) or re.search("......XXX", board) or \
                re.search("X..X..X..", board) or re.search(".X..X..X.", board) or re.search("..X..X..X", board) or \
                re.search("X...X...X", board) or re.search("..X.X.X..", board):
            return "הבלתי מנוצח ניצח!!!!"

        elif re.search("OOO......", board) or re.search("...OOO...", board) or re.search("......OOO", board) or \
                re.search("O..O..O..", board) or re.search(".O..O..O.", board) or re.search("..O..O..O", board) or \
                re.search("O...O...O", board) or re.search("..O.O.O..", board):
            return "ניקול האלופה ניצחה!!!"

        elif "_" in board:  # board.find("_") > -1:
            return "Game not finished"

        else:
            return "לא יאומן זה תיקו!!!"

    def find_immediate_win(self, turn: str) -> (int, int):
        board = self.board_string
        if turn == "X":
            if re.search("XX_......", board) or re.search(".._..X..X", board) \
                    or re.search(".._.X.X..", board):
                return (0, 2)

            elif re.search("X_X......", board) or re.search("._..X..X.", board):
                return (0, 1)

            elif re.search("_XX......", board) or re.search("_...X...X", board) \
                    or re.search("_..X..X..", board):
                return (0, 0)

            elif re.search("..._XX...", board) or re.search("X.._..X..", board):
                return (1, 0)

            elif re.search("...X_X...", board) or re.search(".X.._..X.", board) \
                    or re.search("X..._...X", board) or re.search("..X._.X..", board):
                return (1, 1)

            elif re.search("...XX_...", board) or re.search("..X.._..X", board):
                return (1, 2)

            elif re.search("......_XX", board) or re.search("X..X.._..", board) \
                    or re.search("..X.X._..", board):
                return (2, 0)

            elif re.search("......X_X", board) or re.search(".X..X.._.", board):
                return (2, 1)

            elif re.search("......XX_", board) or re.search("..X..X.._", board) \
                    or re.search("X...X..._", board):
                return (2, 2)

            else:
                return (None, None)

        else:  # turn == "O"
            if re.search("OO_......", board) or re.search(".._..O..O", board) \
                    or re.search(".._.O.O..", board):
                return (0, 2)

            elif re.search("O_O......", board) or re.search("._..O..O.", board):
                return (0, 1)

            elif re.search("_OO......", board) or re.search("_...O...O", board) \
                    or re.search("_..O..O..", board):
                return (0, 0)

            elif re.search("..._OO...", board) or re.search("O.._..O..", board):
                return (1, 0)

            elif re.search("...O_O...", board) or re.search(".O.._..O.", board) \
                    or re.search("O..._...O", board) or re.search("..O._.O..", board):
                return (1, 1)

            elif re.search("...OO_...", board) or re.search("..O.._..O", board):
                return (1, 2)

            elif re.search("......_OO", board) or re.search("O..O.._..", board) \
                    or re.search("..O.O._..", board):
                return (2, 0)

            elif re.search("......O_O", board) or re.search(".O..O.._.", board):
                return (2, 1)

            elif re.search("......OO_", board) or re.search("..O..O.._", board) \
                    or re.search("O...O..._", board):
                return (2, 2)

            else:
                return (None, None)


    def is_empty_square(self, row: int, col: int) -> bool:
        return self.board_array[row][col] == "_"

    # returns a list of free [(row, col)]
    def get_free_coordinates(self) -> [(int, int)]:
        res = []
        for i, row in enumerate(self.board_array):
            for j, cell in enumerate(row):
                if self.is_empty_square(i, j):
                    res.append((i, j))
        return res

    def update(self, row: int, col: int, turn: str) -> bool:
        if self.is_empty_square(row, col):
            self.board_array[row][col] = turn
            self.board_string = self.make_board_string()
            return True
        else:
            return False

    def make_board_string(self) -> str:
        return "".join(["".join(x) for x in self.board_array])


class Player(ABC):

    # TODO: make property
    @abstractmethod
    def description(self):
        pass

    @staticmethod
    @abstractmethod
    def get_move(board: Board, turn: Turn) -> (int, int):
        pass


class UserPlayer(Player):

    _description = "user"

    def description(self):
        return self._description

    @staticmethod
    def __transform_user_coordinates(user_row: int, user_col: int) -> (int, int):
        return user_row - 1, user_col - 1

    @staticmethod
    def get_move(board: Board, turn: Turn) -> (int, int):
        while True:
            # y == row index, x == col index
            coordinates = input("Enter the coordinates: > ").split()
            y, x = coordinates if len(coordinates) == 2 else ("@", "@")
            if not x.isnumeric() or not y.isnumeric():
                print("You should enter numbers!")

            elif not (1 <= int(x) <= 3) or not (1 <= int(y) <= 3):
                print("Coordinates should be from 1 to 3!")

            elif not board.is_empty_square(*UserPlayer.__transform_user_coordinates(int(y), int(x))):
                print("This cell is occupied! Choose another one!")

            else:
                return UserPlayer.__transform_user_coordinates(int(y), int(x))


class NamedUserPlayer(UserPlayer):
    def __init__(self, name="user"):
        self._description = name


class AiPlayer(Player):
    pass


class AiEasyPlayer(AiPlayer):
    _description = "easy"


    def description(self):
        return self._description

    @staticmethod
    def get_move(board: Board, turn: Turn) -> (int, int):
        print(f"Making move level {AiEasyPlayer().description()}")
        return random.choice(board.get_free_coordinates())


class AiMediumPlayer(AiPlayer):

    _description = "medium"

    def description(self):
        return self._description

    @staticmethod
    def get_move(board: Board, turn: Turn) -> (int, int):
        row, col = board.find_immediate_win(turn.current_turn)
        if row is not None:
            return row, col

        row, col = board.find_immediate_win(turn.get_next_turn())
        if row is not None:
            return row, col

        print(f"Making move level {AiMediumPlayer().description()}")
        # return AiEasyPlayer.get_move(board, turn)
        return random.choice(board.get_free_coordinates())


# class MiniMax:
#
#     def __init__(self, board=None):
#         self.__board = Board(board)
#
# not implementing this myself. -.-


class AiHardPlayer(AiPlayer):

    def __init__(self):
        self._description = "hard"
        # super.__init__()      # where did this come from?

    def description(self):
        return self._description


    @staticmethod
    def __translate_board_for_minimax(board: [[str]], minimax_mark: str):
        res = []
        for row in board:
            res_row = []
            for cell in row:
                if cell == "_":
                    res_row.append(".")
                elif cell == "X":
                    res_row.append("O" if minimax_mark == "X" else "X")
                elif cell == "O":
                    res_row.append("X" if minimax_mark == "X" else "O")
            res.append(res_row)
        return res

    @staticmethod
    def get_move(board: Board, turn: Turn) -> (int, int):
        # MiniMax(board)
        m, py, px = Game(AiHardPlayer.__translate_board_for_minimax(board.board_array, turn.current_turn)).max()
        # print(py, px)
        print(f"Making move level {AiHardPlayer().description()}")
        return py, px

class Main:
    def __init__(self, allow_named_users=False):
        self.allow_named_users = allow_named_users
        self.valid_commands = Main.__make_valid_commands([UserPlayer().description(), AiEasyPlayer().description(),
                                                          AiMediumPlayer().description(), AiHardPlayer().description()])

    @staticmethod
    def __make_valid_commands(players: [str]):
        valid_commands = ["exit"]
        for player_1 in players:
            for player_2 in players:
                valid_commands.append(f"start {player_1} {player_2}")
        return valid_commands


    @staticmethod
    def play(player_1: Player, player_2: Player):
        current_board = Board()

        current_player = player_1
        current_turn = Turn("X")

        print(current_board.make_pretty_board())

        # one iteration corresponds to one game turn
        while current_board.get_game_state() == "Game not finished":

            current_y, current_x = current_player.get_move(current_board, current_turn)

            current_board.update(current_y, current_x, current_turn.current_turn)

            print(current_board.make_pretty_board())

            # toggle player
            if current_player == player_1:
                current_player = player_2

            else:
                current_player = player_1

            current_turn.toggle_turn()

        print(current_board.get_game_state())
        print()

    def __is_valid_command(self, command: str):
        return command in self.valid_commands \
               or (self.allow_named_users and command.startswith("start ") and len(command.split()) == 3)

    def __read_command(self) -> str:
        while True:
            command = input("Input command: ")
            if not self.__is_valid_command(command):
                print("Bad parameters!")
            else:
                return command

    def __make_player(self, player_description: str) -> Player:
        if player_description == UserPlayer().description():
            return UserPlayer()
        elif player_description == AiEasyPlayer().description():
            return AiEasyPlayer()
        elif player_description == AiMediumPlayer().description():
            return AiMediumPlayer()
        elif player_description == AiHardPlayer().description():
            return AiHardPlayer()

        else:
            if self.allow_named_users:
                return NamedUserPlayer(player_description)
            else:
                raise ValueError

    def run(self):
        random.seed()
        while True:
            command = self.__read_command()
            if command == "exit":
                exit()
            else:  # start player_1 player_2
                try:
                    self.play(self.__make_player(command.split()[1]), self.__make_player(command.split()[2]))
                except ValueError:
                    print("Bad parameters!")


if __name__ == '__main__':
    Main().run()
    # Main(allow_named_users=True).run()
