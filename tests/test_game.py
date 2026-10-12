from model import Point, Edge, Graph
from controller import GraphController, PlayerController, Game
from game_model import Player
import unittest

from view import GameView


class TestGame(unittest.TestCase):

    """
    test disabeled cuz changed logic
    def test_edge_equality(self):
        p0 = Point((0,0), "P0")
        p1 = Point((0,2), "P1")
        edge_forward = Edge(p0,p1)
        edge_backward = Edge(p1,p0)

        assert edge_forward == edge_backward, "Kanten sollten richtungsunabhängig sein"
    """
    def test_box_completion(self):
        gc = GraphController(grid_size= 5)

        gc.select_edge_point_number(0,1, "red")
        gc.select_edge_point_number(1,4, "red")
        gc.select_edge_point_number(4,3, "red")

        assert gc.check_box(3,0, "red") == 0

        gc.select_edge_point_number(3,0,"red")

        assert gc.check_box(3,0, "red") > 0, "Box sollte geschlossen sein."

    def test_turn_change_logic(self):
        player1 = Player("Red", "red",0)
        player2 = Player("Green", "green",0)
        pc = PlayerController(player1,player2)
        gc = GraphController(grid_size= 5)

        #setze 3 Kanten einer box
        gc.select_edge_point_number(0,1,"red")
        gc.select_edge_point_number(1,4,"red")
        gc.select_edge_point_number(4,3,"red")

        #game initialisieren
        game = Game(gc, pc, view=GameView())
        game.process_turn((3,0))


        # player1 schließt box
        box_closed = gc.check_box(3,0)

        # wenn erfolgreich, soll nicht spieler gewechselt werden
        if not box_closed:
            pc.switch_player()

        assert pc.current_player == player1, "Spieler 1 sollte am zug bleiben, wenn box geschlossen wurde"

    #def test_game_over_condition():
    #gc = GraphController(grid_size=5)
    #hier muss ich noch überlegen. vielleicht while current_points (akkumuliert durch beide player) >= possible_boxes?



    #weitere testidee: check if duplicate selection of graphs is not allowed

