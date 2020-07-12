from .tictactoe import TicTacToe
from .chess import Chess
from .reversi import Reversi

games = {
    TicTacToe().id: TicTacToe(),
    Chess().id: Chess(),
    Reversi().id: Reversi()
}