from .tictactoe import TicTacToe
from .chess import Chess
from .reversi import Reversi
from .mill import Mill

games = {
    TicTacToe().id: TicTacToe(),
    Chess().id: Chess(),
    Reversi().id: Reversi(),
    Mill().id: Mill()
}