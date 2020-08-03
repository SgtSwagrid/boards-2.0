from games.games.tictactoe import TicTacToe
from games.games.chess import Chess
from games.games.reversi import Reversi
from games.games.mill import Mill
from games.games.connectfour import ConnectFour
from games.games.amazons import Amazons
from games.games.dotsandboxes import DotsAndBoxes

games = {
    TicTacToe().id: TicTacToe(),
    Chess().id: Chess(),
    Reversi().id: Reversi(),
    Mill().id: Mill(),
    ConnectFour().id: ConnectFour(),
    Amazons().id: Amazons(),
    DotsAndBoxes().id: DotsAndBoxes()
}