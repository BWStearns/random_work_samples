
class Player(object):
    """
    This is more of a pro-forma separate class since the current build doesn't
    allow any options regarding Players, I broke it out for extensibility and
    code clarity purposes.
    """
    def __init__(self, letter, name=None):
        self.letter = letter
        self.name = name or "Player {0}".format(self.letter)

    def __repr__(self):
        return self.name

    def get_move(self):
        print "{0} Enter your move: ".format(self),
        move = raw_input()
        try:
            move = int(move.strip())
        except:
            move = -1
        return move

class TTTGame(object):
    """
    `TTTGame` manages game state and checks for wins.

    I tried to limit its responsibilities but there could pobably be some
    other class refactored out of this (perhaps not Square as an internal
    class as well.).

    Usage:

    g = TTTGame()
    g.make_move(player_instance, square_number)
    g.game_status
    # => "The battle rages on....."
    """

    class Square(object):
        """
        Using strings for square values seemed wrong.
        """
        def __init__(self, player=None):
            self.player = player

        @property
        def letter(self):
            return self.player.letter if self else "_"

        def __bool__(self):
            return bool(self.player)

        def __nonzero__(self):
            return self.__bool__()

        def __repr__(self):
            return self.letter

        def __eq__(self, other):
            return self.player == other

    ###########################################################################
    # Setup and display
    ###########################################################################

    def __init__(self):
        self.is_draw = False
        self.winner = None
        self.game_finished = False
        self.squares = [[self.Square() for i in range(3)] for j in range(3)]

    def __repr__(self):
        """
        Display code, kinda ugly.
        """
        return """
        \tTICTACTOE
        \t{0}\t{1}\t{2}\n
        \t{3}\t{4}\t{5}\n
        \t{6}\t{7}\t{8}\n
        """.format(*self.individual_squares)

    ###########################################################################
    # Accessors for groups of squares
    ###########################################################################

    @property
    def _verticals(self):
        return zip(*self.squares)

    @property
    def _horizontals(self):
        """
        Kinda dumb to alias but for readability/prima facie logical consistency
        I think it helps.
        """
        return self.squares

    @property
    def _diagonals(self):
        """
        Kinda screwey list comprehensions but it's concise.
        """
        left_right = [r[c] for c,r in enumerate(self.squares)]
        right_left = [r[2-c] for c,r in enumerate(self.squares)]
        return [left_right, right_left]

    @property
    def individual_squares(self):
        return [sq for row in self.squares for sq in row]
    
    @property
    def all_groups(self):
        return self._verticals + self._horizontals + self._diagonals

    ###########################################################################
    # Win checking
    ###########################################################################

    def _check_group_for_win(self, group):
        if not group[0]:
            return False
        if group[0] == group[1] == group[2]:
            return True

    def _check_groups_for_win(self, groups):
        winners = [g for g in groups if self._check_group_for_win(g)]
        return winners[0][0].player if winners else None

    @property
    def board_is_full(self):
        return all(self.individual_squares)

    def _check_for_win(self):
        self.winner = self._check_groups_for_win(self.all_groups)
        self.is_draw = not self.winner and self.board_is_full
        self.game_finished = self.winner or self.is_draw

    @property
    def game_status(self):
        if self.winner:
            return "{0} wins!".format(self.winner)
        if self.is_draw:
            return "It's a draw."
        return "The battle rages on....."

    ###########################################################################
    # Making moves
    ###########################################################################

    def _get_targeted_square(self, target):
        """
        Takes a number 0-8 and returns the value of the square
        """
        return self.squares[target/3][target%3]

    def _set_targeted_square(self, target, player):
        """
        Takes a number 0-8 and sets the value of the square
        """
        self.squares[target/3][target%3].player = player

    def _is_valid_move(self, target):
        """
        Only considers if square is empty, not player turn
        """
        if type(target) == int and (0 <= target < 9):
            return not self._get_targeted_square(target)
        return False

    def make_move(self, player, target):
        """
        - `player` is a Player instance
        - `target` is a number 0-8 which is the square's index top to bottom,
        left to right.

        It updates the `Game.game_status` each change of game state.

        returns `True` if move was executed, `False` if not
        """
        if self._is_valid_move(target) and not self.game_finished:
            self._set_targeted_square(target, player)
            self._check_for_win()
            return True
        else:
            return False


class GameLoop(object):

    def __init__(self, player1=None, player2=None, *args, **kwargs):
        self.players = (
            player1 or Player("X"), 
            player2 or Player("O")
        )
        self.game = TTTGame()
        self.turn = 0

    @property
    def game_status(self):
        return self.game.game_status

    @property
    def game_finished(self):
        return self.game.game_finished

    @property
    def current_player(self):
        return self.players[self.turn % 2]

    def guide_or_scold(self, attempts):
        if attempts == 0:
            return "{0}'s move.... choose wisely".format(self.current_player)
        if attempts <= 2:
            return "Please select a valid move"
        elif attempts > 2:
            return "Dude, you can only select empty squares!"

    def run_game(self):

        game = self.game

        while not self.game_finished:

            current_player = self.current_player
            # Display
            print self.game_status
            print game
            # Check for victory or draw
            if not self.game_finished:
                turn_completed = False
                attempts = 0
                while not turn_completed:
                    # Keep asking for moves until valid
                    print self.guide_or_scold(attempts)
                    attempts += 1
                    move = current_player.get_move()
                    turn_completed = game.make_move(current_player, move)
                self.turn += 1
                continue
            print self.game_status

        print self.game
        print self.game_status

# Initialize and play.
g = GameLoop()
g.run_game()