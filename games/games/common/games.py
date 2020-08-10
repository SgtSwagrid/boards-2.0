from games.games.tictactoe import TicTacToe
from games.games.chess import Chess
from games.games.reversi import Reversi
from games.games.mill import Mill
from games.games.connectfour import ConnectFour
from games.games.amazons import Amazons
from games.games.dotsandboxes import DotsAndBoxes
from games.games.chomp import Chomp
from games.games.clobber import Clobber

games = {
    TicTacToe().ID: TicTacToe(),
    Chess().ID: Chess(),
    Reversi().ID: Reversi(),
    Mill().ID: Mill(),
    ConnectFour().ID: ConnectFour(),
    Amazons().ID: Amazons(),
    DotsAndBoxes().ID: DotsAndBoxes(),
    Chomp().ID: Chomp(),
    Clobber().ID: Clobber()
}