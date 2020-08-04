from .common.game import *
from .common.handler import *


# note to self: phase 1 through 3 are hardcoded conditionals rather than actual variables
# TODO replace above circumstance with usage of state.epoch
#   am at it:
#   epoch 0 implemented
#   epoch 1 partially implemented:
#     missing flying
# TODO add mill recognition


class Mill(Game):
    name = "Mill"
    id = 4
    width = 11
    height = 11
    players = 2

    class Graph:

        class Node:

            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.neighbours = []

            def add_neighbour(self, other):
                if other not in self.neighbours:
                    self.neighbours.append(other)

            def is_neighbour(self, other):
                return other in self.neighbours

        def __init__(self):
            self.nodes = []

        def add_node(self, x, y):
            self.nodes.append(self.Node(x, y))

        def add_edge(self, node, node_list):
            for point in node_list:
                node.add_neighbour(point)
                point.add_neighbour(node)

        def fetch_node(self, x, y):
            for point in self.nodes:
                if x == point.x and y == point.y:
                    return point

        def is_node(self, x, y):
            return self.fetch_node(x, y) in self.nodes

        def is_mill(self, state, piece):
            # if the current player owns all pieces alongside the respective y-axis or the x-axis they achieved a mill
            print([piece.x, piece.y])
            print([state.pieces[point.x][point.y] and state.turn.current == state.pieces[point.x][point.y].owner
                   for point in self.nodes if point.x == piece.x])
            print([state.pieces[point.x][point.y] and state.turn.current == state.pieces[point.x][point.y].owner
                   for point in self.nodes if point.y == piece.y])
            if all([state.pieces[point.x][point.y] and state.turn.current == state.pieces[point.x][point.y].owner
                    for point in self.nodes if point.x == piece.x]) \
                    or all(
                [state.pieces[point.x][point.y] and state.turn.current == state.pieces[point.x][point.y].owner
                 for point in self.nodes if point.y == piece.y]):
                print('MILL!')
                return True

    graph = Graph()

    validPoint = [
        (0, 10), (0, 5), (0, 0), (2, 8), (2, 5), (2, 2), (4, 6), (4, 5), (4, 4), (5, 10), (5, 8), (5, 6), (5, 4),
        (5, 2), (5, 0), (6, 6), (6, 5), (6, 4), (8, 8), (8, 5), (8, 2), (10, 10), (10, 5), (10, 0)
    ]

    for point in validPoint:
        graph.add_node(point[0], point[1])

    graph.add_edge(graph.fetch_node(0, 10), [graph.fetch_node(5, 10), graph.fetch_node(0, 5)])
    graph.add_edge(graph.fetch_node(5, 10), [graph.fetch_node(5, 8), graph.fetch_node(10, 10)])
    graph.add_edge(graph.fetch_node(10, 10), [graph.fetch_node(10, 5)])

    graph.add_edge(graph.fetch_node(2, 8), [graph.fetch_node(5, 8), graph.fetch_node(2, 5)])
    graph.add_edge(graph.fetch_node(5, 8), [graph.fetch_node(5, 6), graph.fetch_node(8, 8)])
    graph.add_edge(graph.fetch_node(8, 8), [graph.fetch_node(8, 5)])

    graph.add_edge(graph.fetch_node(4, 6), [graph.fetch_node(4, 5), graph.fetch_node(5, 6)])
    graph.add_edge(graph.fetch_node(5, 6), [graph.fetch_node(6, 6)])
    graph.add_edge(graph.fetch_node(6, 6), [graph.fetch_node(6, 5)])

    graph.add_edge(graph.fetch_node(0, 5), [graph.fetch_node(0, 0), graph.fetch_node(2, 5)])
    graph.add_edge(graph.fetch_node(2, 5), [graph.fetch_node(2, 2), graph.fetch_node(4, 5)])
    graph.add_edge(graph.fetch_node(4, 5), [graph.fetch_node(4, 4)])

    graph.add_edge(graph.fetch_node(0, 0), [graph.fetch_node(5, 0)])
    graph.add_edge(graph.fetch_node(2, 2), [graph.fetch_node(5, 2)])
    graph.add_edge(graph.fetch_node(4, 4), [graph.fetch_node(5, 4)])

    graph.add_edge(graph.fetch_node(5, 4), [graph.fetch_node(5, 2), graph.fetch_node(6, 4)])
    graph.add_edge(graph.fetch_node(5, 2), [graph.fetch_node(5, 0), graph.fetch_node(8, 2)])
    graph.add_edge(graph.fetch_node(5, 0), [graph.fetch_node(10, 0)])

    graph.add_edge(graph.fetch_node(6, 5), [graph.fetch_node(6, 4), graph.fetch_node(8, 5)])
    graph.add_edge(graph.fetch_node(8, 5), [graph.fetch_node(8, 2), graph.fetch_node(10, 5)])
    graph.add_edge(graph.fetch_node(10, 5), [graph.fetch_node(10, 0)])

    # designates every tile which qualifies as a connection, important for assigning the textures in display
    connections = []
    for x in range(0, width):
        for y in range(0, height):
            if x == 0 or x == (width - 1) or y == 0 or y == (height - 1):
                connections.append((x, y))
            elif (y == 2 or y == (height - 3)) and 1 < x < (width - 2):
                connections.append((x, y))
            elif (x == 2 or x == (width - 3)) and 1 < y < (height - 2):
                connections.append((x, y))
            elif (y == 4 or y == (height - 5)) and 3 < x < (width - 4):
                connections.append((x, y))
            elif y == 5 and x != 5:
                connections.append((x, y))
            elif y != 5 and x == 5:
                connections.append((x, y))

    class MillPiece(PieceType):
        id = 0

        def texture(self, piece, state, display):
            if piece.owner == 0:
                return Texture('games/img/misc/white_dot.png')
            else:
                return Texture('games/img/misc/black_dot.png')

    types = [MillPiece()]

    handlers = [PlaceHandler(MillPiece()), MoveHandler(), RemoveHandler()]

    #  drawing colors for (1)tiles/points where pieces can be (2)tiles/lines in between and (3)every other tile
    def background_colour(self, x, y):
        return '#FFEAA7'

    def display(self, state, display):
        for x in range(0, self.width):
            for y in range(0, self.height):
                # tests that only connection tiles get to be shown as connections
                if (x, y) in self.connections:
                    # tests whether a tile needs to be marked as a valid point to be moved one
                    if self.graph.is_node(x, y):
                        texture = 'games/img/mill/dot.png'
                        display = display.add_texture(x, y, Texture(texture))
                    # tests whether a tile has neighbours it needs to be connected to
                    if (x + 1, y) in self.connections:
                        texture = 'games/img/mill/half_line_right.png'
                        display = display.add_texture(x, y, Texture(texture))
                    if (x - 1, y) in self.connections:
                        texture = 'games/img/mill/half_line_left.png'
                        display = display.add_texture(x, y, Texture(texture))
                    if (x, y + 1) in self.connections:
                        texture = 'games/img/mill/half_line_up.png'
                        display = display.add_texture(x, y, Texture(texture))
                    if (x, y - 1) in self.connections:
                        texture = 'games/img/mill/half_line_down.png'
                        display = display.add_texture(x, y, Texture(texture))
        display = super().display(state, display)
        return display

    # a piece of the active player can be placed iff not all pieces have been placed yet
    def place_valid(self, state, piece):
        # if epoch is placing epoch and the selected tile is valid and there is no other piece already
        if state.turn.epoch == 0:
            return self.graph.is_node(piece.x, piece.y) and not state.pieces[piece.x][piece.y]
        else:
            return False

    # in case all pieces are placed, that means both players have a score of 9, the epoch advances and no more pieces
    # shall be placed
    def place_piece(self, state, piece):
        state = state.place_piece(piece).add_score(state.turn.current, 1)
        if state.players[state.turn.current].score == state.players[1 - state.turn.current].score >= 9:
            state = state.end_epoch()
        return state.end_turn()

    # a piece owned by the active player can be moved iff all pieces have already been placed = after turn 17
    def move_valid(self, state, piece, x_to, y_to):
        if state.turn.epoch == 1 and state.turn.stage == 0:
            # if in the graph from the starting node the target node is reachable and there is no other piece yet
            if self.graph.fetch_node(piece.x, piece.y).is_neighbour(self.graph.fetch_node(x_to, y_to)) and not \
                    state.pieces[x_to][y_to]:
                return True
        else:
            return False

    # after moving a piece a NEW mill might have been formed iff that is the case remove one opponents piece
    def move_piece(self, state, piece, x_to, y_to):
        state = state.move_piece(piece, x_to, y_to)
        # TODO: some parts will be calculated before, others after having moved that piece, this leads to wrong
        #  recognition,
        #  also the middle things are not working as intended and consider all 6 instead of only the 3 connected nodes,
        #  maybe it's above me to do list comprehension, maybe I need to sleep before
        print([x_to, y_to])
        if not self.graph.is_mill(state, piece):
            return state.end_turn()
        else:
            return state.end_stage()

    #  a piece may only removed IFF a mill has been formed before(state.stage == 1) and it's an opponent's
    def remove_valid(self, state, piece):
        return state.turn.stage == 1 and state.enemy(piece.x, piece.y)
