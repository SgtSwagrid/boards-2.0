from .common.game import *


class MillPiece(PieceType):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    # a piece of the active player can be placed iff not all pieces have been placed yet
    def place_valid(self, state, piece):
        # if epoch is placing epoch and the selected tile is valid and there is no other piece already
        if state.turn.epoch == 0 and state.turn.stage == 0:
            return state.game.graph.is_node(piece.pos) and not state.piece(piece.pos)
        else:
            return False

    # in case all pieces are placed, that means both players have a score of 9, the epoch advances and no more pieces
    # shall be placed
    def place_piece(self, state, piece):
        state = state.place_piece(piece).add_score(state.turn.current_id, 1)
        if state.turn.ply / 2 > 8:
            state = state.end_epoch()
        #print(state.turn.ply / 2)
        piece = state.piece(piece.pos)
        if state.game.graph.is_mill(state, piece):
            #print('end stage')
            return state.end_stage()
        else:
            #print('end turn')
            return state.end_turn()

    # a piece owned by the active player can be moved iff all pieces have already been placed = after turn 17
    def move_valid(self, state, piece, pos):
        if state.turn.epoch == 1 and state.turn.stage == 0:
            # if in the graph from the starting node the target node is reachable and there is no other piece yet
            if state.game.graph.fetch_node(piece.x, piece.y).is_neighbour(state.game.graph.fetch_node(pos)) and not \
                    state.piece(pos):
                return True
        else:
            return False

    # after moving a piece a NEW mill might have been formed iff that is the case remove one opponents piece
    def move_piece(self, state, piece, pos):
        state = state.move_piece(piece, pos)
        piece = state.piece(pos)
        # print([x_to, y_to])
        # print([piece.x, piece.y])
        if not state.game.graph.is_mill(state, piece):
            return state.end_turn()
        else:
            return state.end_stage()

    #  a piece may only removed IFF a mill has been formed before(state.stage == 1) and it's an opponent's
    def remove_valid(self, state, piece):
        try:
            return state.turn.stage == 1 and state.enemy(piece.pos)
        except AttributeError:
            return False

    def remove_piece(self, state, piece):
        state = state.remove_piece(piece)
        state = state.add_score(state.turn.next_id, -1)
        return state.end_turn()


class MillBackground(Background):

    def __init__(self, colours, graph, width, height):
        super().__init__(colours)
        self.GRAPH = graph
        # designates every tile which qualifies as a connection, important for assigning the textures in display
        self.connections = []
        for x in range(0, width):
            for y in range(0, height):
                pos = Vec(x, y)
                if pos.x == 0 or pos.x == (width - 1) or pos.y == 0 or pos.y == (height - 1):
                    self.connections.append(pos)
                elif (pos.y == 2 or pos.y == (height - 3)) and 1 < pos.x < (width - 2):
                    self.connections.append(pos)
                elif (pos.x == 2 or pos.x == (width - 3)) and 1 < pos.y < (height - 2):
                    self.connections.append(pos)
                elif (pos.y == 4 or pos.y == (height - 5)) and 3 < pos.x < (width - 4):
                    self.connections.append(pos)
                elif pos.y == 5 and pos.x != 5:
                    self.connections.append(pos)
                elif pos.y != 5 and pos.x == 5:
                    self.connections.append(pos)

    def colour(self, pos):
        return '#FFEAA7'

    def texture(self, pos):
        textures = []
        # tests that only connection tiles get to be shown as connections
        if pos in self.connections:
            # tests whether a tile needs to be marked as a valid point to be moved one
            if self.GRAPH.is_node(pos):
                textures.append('mill/dot.png')
            # tests whether a tile has neighbours it needs to be connected to
            if pos + (1, 0) in self.connections:
                textures.append('mill/half_line_right.png')
            if pos - (1, 0) in self.connections:
                textures.append('mill/half_line_left.png')
            if pos + (0, 1) in self.connections:
                textures.append('mill/half_line_up.png')
            if pos - (0, 1) in self.connections:
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

            def __init__(self, pos):
                self.pos = pos
                self.neighbours = []

            def add_neighbour(self, other):
                if other not in self.neighbours:
                    self.neighbours.append(other)

            def is_neighbour(self, other):
                return other in self.neighbours

        def __init__(self):
            self.nodes = []

        def add_node(self, pos):
            self.nodes.append(self.Node(pos))

        def add_edge(self, pos, pos_list):
            node = self.fetch_node(pos)
            for point_pos in pos_list:
                point = self.fetch_node(point_pos)
                node.add_neighbour(point)
                point.add_neighbour(node)

        def fetch_node(self, pos=None, piece=None):
            if piece is None:
                for point in self.nodes:
                    if pos == point.pos:
                        return point
            else:
                for point in self.nodes:
                    if piece.pos == point.pos:
                        return point

        def is_node(self, pos):
            return self.fetch_node(pos) in self.nodes

        def is_mill(self, state, piece):
            mill_x_friend = None
            mill_y_friend = None
            for neighbour in self.fetch_node(piece=piece).neighbours:
                # print(str(neighbour.x) + ' | ' + str(neighbour.y))
                if state.piece(neighbour.pos):
                    neighbour_piece = state.piece(neighbour.pos)
                    if neighbour_piece.owner_id == state.turn.current_id:
                        # print('True')
                        # these so called duplicates are actually not duplicates at all ...
                        if not mill_x_friend:
                            if neighbour_piece.pos.x == piece.pos.x:
                                # print('Make a friend in x')
                                mill_x_friend = neighbour_piece
                        elif neighbour_piece is not piece and mill_x_friend.pos.x == neighbour_piece.pos.x:
                            #print([[mill_x_friend.x, mill_x_friend.y], [neighbour_piece.x, neighbour_piece.y]])
                            return True

                        if not mill_y_friend:
                            if neighbour_piece.pos.y == piece.pos.y:
                                # print('Make a friend in y')
                                mill_y_friend = neighbour_piece
                        elif neighbour_piece is not piece and mill_y_friend.pos.y == neighbour_piece.pos.y:
                            #print([[mill_y_friend.x, mill_y_friend.y], [neighbour_piece.x, neighbour_piece.y]])
                            return True

                        for more_neighbour in self.fetch_node(piece=neighbour_piece).neighbours:
                            # print(str(more_neighbour.x) + ' | ' + str(more_neighbour.y))
                            if state.piece(more_neighbour.pos):
                                neighbour_piece = state.piece(more_neighbour.pos)
                                if neighbour_piece.owner_id == state.turn.current_id and \
                                        (piece.pos == more_neighbour.pos) and \
                                        (neighbour_piece is not piece):
                                    #print([[piece.x, piece.y], [neighbour_piece.x, neighbour_piece.y]])
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
        Vec(0, 10), Vec(0, 5), Vec(0, 0), Vec(2, 8), Vec(2, 5), Vec(2, 2), Vec(4, 6), Vec(4, 5), Vec(4, 4),
        Vec(5, 10), Vec(5, 8), Vec(5, 6), Vec(5, 4), Vec(5, 2), Vec(5, 0), Vec(6, 6), Vec(6, 5), Vec(6, 4),
        Vec(8, 8), Vec(8, 5), Vec(8, 2), Vec(10, 10), Vec(10, 5), Vec(10, 0)
    ]

    for point in validPoint:
        graph.add_node(point)

    graph.add_edge(Vec(0, 10), [Vec(5, 10), Vec(0, 5)])
    graph.add_edge(Vec(5, 10), [Vec(5, 8), Vec(10, 10)])
    graph.add_edge(Vec(10, 10), [Vec(10, 5)])

    graph.add_edge(Vec(2, 8), [Vec(5, 8), Vec(2, 5)])
    graph.add_edge(Vec(5, 8), [Vec(5, 6), Vec(8, 8)])
    graph.add_edge(Vec(8, 8), [Vec(8, 5)])

    graph.add_edge(Vec(4, 6), [Vec(4, 5), Vec(5, 6)])
    graph.add_edge(Vec(5, 6), [Vec(6, 6)])
    graph.add_edge(Vec(6, 6), [Vec(6, 5)])

    graph.add_edge(Vec(0, 5), [Vec(0, 0), Vec(2, 5)])
    graph.add_edge(Vec(2, 5), [Vec(2, 2), Vec(4, 5)])
    graph.add_edge(Vec(4, 5), [Vec(4, 4)])

    graph.add_edge(Vec(0, 0), [Vec(5, 0)])
    graph.add_edge(Vec(2, 2), [Vec(5, 2)])
    graph.add_edge(Vec(4, 4), [Vec(5, 4)])

    graph.add_edge(Vec(5, 4), [Vec(5, 2), Vec(6, 4)])
    graph.add_edge(Vec(5, 2), [Vec(5, 0), Vec(8, 2)])
    graph.add_edge(Vec(5, 0), [Vec(10, 0)])

    graph.add_edge(Vec(6, 5), [Vec(6, 4), Vec(8, 5)])
    graph.add_edge(Vec(8, 5), [Vec(8, 2), Vec(10, 5)])
    graph.add_edge(Vec(10, 5), [Vec(10, 0)])

    PIECES = [MillPiece()]
    HANDLERS = [PlaceHandler(MillPiece()), MoveHandler(PIECES), RemoveHandler(PIECES)]
    # needs to be here so it can take "graph" as an argument
    BACKGROUND = MillBackground(['#FFEAA7'], graph, 11, 11)

    def on_action(self, state):

        #print([state.turn.next_id, state.player_states[state.turn.next_id].score],
        #      [state.turn.current_id, state.player_states[state.turn.current_id].score],
        #      state.turn.epoch)
        if state.player_states[state.turn.current_id].score < 3 and state.turn.epoch > 0:
            state = state.end_game(state.turn.next_id)

        return state
