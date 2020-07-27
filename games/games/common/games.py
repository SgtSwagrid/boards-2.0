from games.games.tictactoe import TicTacToe
from games.games.chess import Chess
from games.games.reversi import Reversi
from games.games.mill import Mill

games = {
    TicTacToe().id: TicTacToe(),
    Chess().id: Chess(),
    Reversi().id: Reversi(),
    Mill().id: Mill()
}