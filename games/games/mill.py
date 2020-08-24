from .common.game import *


class MillBoardBackground(Background):

    def __init__(self, colours, graph, width, height):
        super().__init__(colours)
        self.GRAPH = graph
        # designates every tile which qualifies as a connection, important for assigning the textures in display
        self.connections = []
        for x in range(0, width):
            for y in range(0, height):
                if x == 0 or x == (width - 1) or y == 0 or y == (height - 1):
                    self.connections.append((x, y))
                elif (y == 2 or y == (height - 3)) and 1 < x < (width - 2):
                    self.connections.append((x, y))
                elif (x == 2 or x == (width - 3)) and 1 < y < (height - 2):
                    self.connections.append((x, y))
                elif (y == 4 or y == (height - 5)) and 3 < x < (width - 4):
                    self.connections.append((x, y))
                elif y == 5 and x != 5:
                    self.connections.append((x, y))
                elif y != 5 and x == 5:
                    self.connections.append((x, y))

    def colour(self, x, y):
        return '#FFEAA7'

    def texture(self, x, y):
        textures = []
        # tests that only connection tiles get to be shown as connections
        if (x, y) in self.connections:
            # tests whether a tile needs to be marked as a valid point to be moved one
            if self.GRAPH.is_node(x, y):
                textures.append('mill/dot.png')
            # tests whether a tile has neighbours it needs to be connected to
            if (x + 1, y) in self.connections:
                textures.append('mill/half_line_right.png')
            if (x - 1, y) in self.connections:
                textures.append('mill/half_line_left.png')
            if (x, y + 1) in self.connections:
                textures.append('mill/half_line_up.png')
            if (x, y - 1) in self.connections:
                textures.append('mill/half_line_down.png')
        return textures


class Mill(Game):
    ID = 4
    NAME = 'Mill'
    SHAPE = Rectangle(11, 11)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Nine_men%27s_morris'

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

        def fetch_node(self, x=None, y=None, piece=None):
            if piece is None:
                for point in self.nodes:
                    if x == point.x and y == point.y:
                        return point
            else:
                for point in self.nodes:
                    if piece.x == point.x and piece.y == point.y:
                        return point

        def is_node(self, x, y):
            return self.fetch_node(x, y) in self.nodes

        def is_mill(self, state, piece):
            mill_x_friend = None
            mill_y_friend = None
            for neighbour in self.fetch_node(piece=piece).neighbours:
                # print(str(neighbour.x) + ' | ' + str(neighbour.y))
                if state.pieces[neighbour.x][neighbour.y]:
                    neighbour_piece = state.pieces[neighbour.x][neighbour.y]
                    if neighbour_piece.owner_id == state.turn.current_id:
                        # print('True')
                        # these so called duplicates are actually not duplicates at all ...
                        if not mill_x_friend:
                            if neighbour_piece.x == piece.x:
                                # print('Make a friend in x')
                                mill_x_friend = neighbour_piece
                        elif neighbour_piece is not piece and mill_x_friend.x == neighbour_piece.x:
                            print([[mill_x_friend.x, mill_x_friend.y], [neighbour_piece.x, neighbour_piece.y]])
                            return True

                        if not mill_y_friend:
                            if neighbour_piece.y == piece.y:
                                # print('Make a friend in y')
                                mill_y_friend = neighbour_piece
                        elif neighbour_piece is not piece and mill_y_friend.y == neighbour_piece.y:
                            print([[mill_y_friend.x, mill_y_friend.y], [neighbour_piece.x, neighbour_piece.y]])
                            return True

                        for more_neighbour in self.fetch_node(piece=neighbour_piece).neighbours:
                            # print(str(more_neighbour.x) + ' | ' + str(more_neighbour.y))
                            if state.pieces[more_neighbour.x][more_neighbour.y]:
                                neighbour_piece = state.pieces[more_neighbour.x][more_neighbour.y]
                                if neighbour_piece.owner_id == state.turn.current_id and \
                                        (piece.x == neighbour_piece.x or piece.y == neighbour_piece.y) and \
                                        (neighbour_piece is not piece):
                                    print([[piece.x, piece.y], [neighbour_piece.x, neighbour_piece.y]])
                                    # print('True')
                                    return True
                #                 else:
                #                     print('False')
                #             else:
                #                 print('False')
                #     else:
                #         print('False')
                # else:
                #     print('False')
            return False

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

    class MillPiece(PieceType):
        ID = 0
        TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    PIECES = [MillPiece()]
    HANDLERS = [PlaceHandler(MillPiece()), MoveHandler(), RemoveHandler()]
    # needs to be here so it can take "graph" as an argument
    BACKGROUND = MillBoardBackground(['#FFEAA7'], graph, 11, 11)

    # a piece of the active player can be placed iff not all pieces have been placed yet
    def place_valid(self, state, piece):
        # if epoch is placing epoch and the selected tile is valid and there is no other piece already
        if state.turn.epoch == 0 and state.turn.stage == 0:
            return self.graph.is_node(piece.x, piece.y) and not state.pieces[piece.x][piece.y]
        else:
            return False

    # in case all pieces are placed, that means both players have a score of 9, the epoch advances and no more pieces
    # shall be placed
    def place_piece(self, state, piece):
        state = state.place_piece(piece).add_score(state.turn.current_id, 1)
        if state.turn.ply / 2 > 8:
            state = state.end_epoch()
        print(state.turn.ply / 2)
        piece = state.pieces[piece.x][piece.y]
        if self.graph.is_mill(state, piece):
            print('end stage')
            return state.end_stage()
        else:
            print('end turn')
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
        piece = state.pieces[x_to][y_to]
        # print([x_to, y_to])
        # print([piece.x, piece.y])
        if not self.graph.is_mill(state, piece):
            return state.end_turn()
        else:
            return state.end_stage()

    #  a piece may only removed IFF a mill has been formed before(state.stage == 1) and it's an opponent's
    def remove_valid(self, state, piece):
        try:
            return state.turn.stage == 1 and state.enemy(piece.x, piece.y)
        except AttributeError:
            return False

    def remove_piece(self, state, piece):
        state = state.remove_piece(piece)
        state = state.add_score(state.turn.next_id, -1)
        return state.end_turn()

    def action(self, state, action):
        print([state.turn.next_id, state.player_states[state.turn.next_id].score],
              [state.turn.current_id, state.player_states[state.turn.current_id].score],
              state.turn.epoch)
        if state.player_states[state.turn.current_id].score < 3 and state.turn.epoch > 0:
            state = state.end_game(state.turn.next_id)

        return state
