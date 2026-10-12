from Agents.agent_alphabeta import AgentAlphaBeta
from State.problem import GameState
from Agents.agent_von_Vorlesung import agentvV
from model import Graph, Point, Edge, Box
from view import GameView
from game_model import Player, RandomNPC, HumanPlayer, AgentPlayer
from Agents.minimax_agent import AgentMinimax



class GraphController:
    """
    Spezifische Logik für ein Spiel, das ein 5x5-Grid verwendet.
    Nutzt intern einen allgemeinen Graphen (GameGraph).
    Angenommen, bei einem 5x5-Raster (UI-Raster mit Knoten und Kanten) ergeben sich 9 Knoten, die folgendermaßen
    angeordnet sind (zeilenweise):
    0   1   2
    3   4   5
    6   7   8
   """
   

#konstruktor für die spiellogik. hier: 5x5 grid
#warum 5x5?: es werden gerade koordinaten als spielfelder verwendet, ungerade als raum für die linien.
    def __init__(self, grid_size: int = 5) -> None:
        self.graph = Graph()
        self.grid_size = grid_size
        
        
        #NEW: dictionary. wieso keine liste? liste kann in python kein key sein. (siehe box_check logik)
        #dynamisch umgesetztes dictionary
       
        # N = punkte pro seite (zb 3 bei grid size 5)
        self.n_points_per_side = (self.grid_size //2) + 1
        #max punkte (N-1)^2 (zb 4 bei n = 3)
        self.max_points = (self.n_points_per_side - 1) ** 2
        
        self.setup_grid()
        self.boxes_affected_by_edge = self._generate_edges_to_boxes()[0]
        self.edges_part_of_box = self._generate_edges_to_boxes()[1]
        self.last_selected_edge = None
        self.boxes = {}
        for b_id, edges in self.edges_part_of_box.items():
            self.boxes[b_id] = Box(edges=edges, id=b_id)

    """Generiert die Zuordnung von Kanten zu Boxen und umgekehrt."""
    def _generate_edges_to_boxes(self) -> tuple[dict, dict]:
        #überlegung: N = anzahl punkte pro seite (zb 3 bei grid_size = 5)
        N = self.n_points_per_side
        num_boxes_per_side = N - 1
        edge_map = {}
        box_map = {}

        #alle möglichen boxen finden
        # r = rows
        for r in range(num_boxes_per_side):
            # c = colms
            for c in range(num_boxes_per_side):
                #eindeutige id für box beispiel:  r= 0, c= 0 ID=0 etc
                box_id = r * num_boxes_per_side + c

                #4 ecken der box berechnen
                top_left = self.graph.nodes[r * N + c]
                top_right = self.graph.nodes[r * N + c+1]
                bottom_left = self.graph.nodes[(r + 1) * N + c]
                bottom_right = self.graph.nodes[(r + 1) * N + c+1]

                edges = [
                    Edge(top_left,top_right), #oben (zb 0-1)
                    Edge(bottom_left, bottom_right), #unten (zb 3-4)
                    Edge(top_left, bottom_left), #links (zb 0-3)
                    Edge(top_right, bottom_right) #rechts (zb 1-4)
                ]

                #rein ins box dictionary
                box_map[box_id] = [edge for edge in self.graph.get_edges() if edge in edges]
                #rein ins dictionary
                for e in edges:
                    if e not in edge_map:
                        edge_map[e] = []
                    edge_map[e].append(box_id)
                    #geben jeweils 2 maps zurück für bidirektionale suche
        return edge_map, box_map

    #funktion für das aufstellen des grids anhand gewuenschter grid_size.
    def setup_grid(self) -> None:
        point_index = 0
        # Knoten an den "geraden" Positionen hinzufügen.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i % 2 == 0 and j % 2 == 0:
                    node = Point((i, j), f"P{point_index}")
                    self.graph.add_node(node)
                    point_index += 1
        self.add_edges()

    #funktion fürs logische hinzufügen von edges in unseren graphen.
    def add_edges(self) -> None:

        points = self.graph.nodes
        if len(points) == 9:
            edges = [
                Edge(points[0], points[1]), Edge(points[0], points[3]),
                Edge(points[1], points[2]), Edge(points[1], points[4]),
                Edge(points[2], points[5]), Edge(points[3], points[4]),
                Edge(points[3], points[6]), Edge(points[4], points[5]),
                Edge(points[4], points[7]), Edge(points[5], points[8]),
                Edge(points[6], points[7]), Edge(points[7], points[8])
            ]

            for edge in edges:
                self.graph.add_edge(edge.point_one, edge.point_two)

    #tuersteher funktion: nimmt zwei points, die eine edge ausmachen
    def __select_edge(self, a: Point, b: Point, color: str) -> bool:
        edge = Edge(a, b)
        edges = self.graph.get_edges()
        #wir schauen ob die edge schon gespielt wurde
        for e in edges:
            if edge == e:
                if e.selected:
                    return False
                e.select(color)
                #merken was der letzte zug war
                self.last_selected_edge = e
                return True

        return False
    #public class um eingabe in points zu verwandeln.
    def select_edge_point_number(self, a: int, b: int, color: str):
        return self.__select_edge(self.graph.nodes[a],
                                  self.graph.nodes[b],
                                  color)

#NEW: added checkbox logic
#p1_index, p2_index kommen aus Game.start()
    def check_box(self,p1_index: int, p2_index: int, color:str) -> int:
       #normalisiere Key
       edge = Edge(self.graph.nodes[p1_index], self.graph.nodes[p2_index])

       affected_boxes = self.boxes_affected_by_edge.get(edge, [])
       points_earned = 0


        #count up
       for b_id in affected_boxes:
           box = self.boxes[b_id]
           
           if box.conquered:
               continue
           counter = sum(1 for e in box.edges if e.selected)
        # ist box voll?
           if counter == 4:
               box.conquered = True
               box.color = color
               points_earned += 1
               
       return points_earned

    #Hilfsfunktion um noch nicht gemalte Kanten zu ermitteln
    def get_available_moves(self) -> list[tuple[int,int]]:
        available = []
        for edge in self.graph.get_edges():
            if not edge.selected:
                p1_num = self.graph.nodes.index(edge.point_one)
                p2_num = self.graph.nodes.index(edge.point_two)
                available.append((p1_num, p2_num))
        return available






    def __repr__(self) -> str:
        return repr(self.graph)
    

#Klasse für die Spielersteuerung, die die aktuelle Spielerfarbe und die Logik für den Spielerwechsel verwaltet.
class PlayerController:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
    #getted unsere gezeichnete linie von knoten zu knoten aus game model eingabe
    def get_player_edge(self, game_state: GameState):
        edge = self.current_player.get_move(game_state)
        return edge
    #Wechsel player 
    def switch_player(self):
        tmp = self.current_player
        self.current_player = self.other_player
        self.other_player = tmp
    #holt sich die farbe von current_player
    def get_color(self):
        return self.current_player.color

#NEW: validierung der inputs
def validate_input(edge):
    try:
        p1 = int(edge[0])
        p2 = int(edge[1])
        return p1, p2
    except (ValueError, IndexError):
        print("Invalid Input!")
        return None

#Klasse für die gesamte Spiellogik, die die Interaktion zwischen GraphController, PlayerController und GameView steuert.
class Game:
    def __init__(self, graph_controller: GraphController,
                 player_controller: PlayerController,
                 view: GameView,
                 game_state: GameState):
        self.game_state = game_state
        self.graph_controller = graph_controller
        self.player_controller = player_controller
        self.view = view

    #Methode, die einen Spielzug verarbeitet: Validierung der Eingabe, Aktualisierung des Graphen, Überprüfung auf abgeschlossene Boxen, Punktevergabe und Spielerwechsel.
    def process_turn(self, edge):

        p1, p2 = edge
        #NEW: Sicherstellen, dass nur Edges in eine Richtung angesprochen werden.
        if p1 > p2:
            p1, p2 = p2, p1
          # 1. Farbe vom aktuellen Spieler holen
        current_color = self.player_controller.get_color()

        if (p1, p2) not in self.game_state.all_edges:
            print("Edge is already drawn, or doesn't exist")
            self._sync_game_state_from_graph()
            return
        
        # 2. current_color an select_edge übergeben
        if self.graph_controller.select_edge_point_number(p1, p2, current_color):
            
            # 3. current_color an check_box übergeben
            new_points = self.graph_controller.check_box(p1, p2, current_color)
            if new_points > 0:
                self.player_controller.current_player.points += new_points
                print(f"Score! {self.player_controller.current_player.name} earned {new_points} Point(s)")
                #Kein switch_player -> spieler darf nochmal ziehen
            else:
                #analog kein punkt -> switch player
                self.player_controller.switch_player()
            self._sync_game_state_from_graph()
            self.view.display(self.graph_controller.grid_size, 
                              self.graph_controller.graph.adjacency, 
                              self.graph_controller.boxes)

        else:
            print("Edge is already drawn, or doesn't exist")
            self._sync_game_state_from_graph()

    def _sync_game_state_from_graph(self) -> None:
        drawn_edges = set()

        for edge in self.graph_controller.graph.get_edges():
            if edge.selected:
                p1 = self.graph_controller.graph.nodes.index(edge.point_one)
                p2 = self.graph_controller.graph.nodes.index(edge.point_two)
                if p1 > p2:
                    p1, p2 = p2, p1
                drawn_edges.add((p1, p2))

        all_edges = self.game_state.all_edges
        not_drawn_edges = all_edges - drawn_edges

        current_player = self.player_controller.get_color()
        scores = (
            self.player_controller.player1.points,
            self.player_controller.player2.points
        )

        self.game_state = GameState(
            drawn_edges=frozenset(drawn_edges),
            not_drawn_edges=frozenset(not_drawn_edges),
            current_player=current_player,
            scores=scores,
            all_edges=all_edges
        )



    #Methode, die den Hauptspielzyklus steuert: Solange das Spiel nicht vorbei ist, fordert sie den aktuellen Spieler auf, einen Zug zu machen, verarbeitet diesen Zug und aktualisiert die Anzeige. Am Ende des Spiels zeigt sie die Ergebnisse an.
    def start(self):
        #Fix: rudimentäre abbruchbedingung, bei 3x3 grid sind nur 4 boxes möglich.
        for edge in self.game_state.drawn_edges:
            self.graph_controller.select_edge_point_number(edge[0], edge[1], self.player_controller.get_color())
        self._sync_game_state_from_graph()
        while len(self.graph_controller.get_available_moves()) > 0:
            edge = self.player_controller.get_player_edge(self.game_state)
            self.process_turn(edge)

                
        #game end results
        print("\n--- GAME OVER ---")
        p1, p2 = self.player_controller.player1, self.player_controller.player2
        print(f"Endstand: {p1.name} ({p1.points}) : {p2.name} ({p2.points})")

# Hauptfunktion, die die Spieler auswählt, das Spiel initialisiert und startet.
if __name__ == "__main__":
    print("--- Welcome to Dots and Boxes ---")
    print("Choose your game mode:")
    print("1. Human vs Human")
    print("2. Human vs NPC")
    print("3. NPC vs NPC")
    print("4. Agent Run")
    print("5. Agent Minimax")
    print("6. Human vs Minimax")
    print("7. AlphaBeta vs AlphaBeta")
    print("8. Human vs AlphaBeta")
    
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        player1 = HumanPlayer("Player 1", "red")
        player2 = HumanPlayer("Player 2", "green")
    elif choice == "2":
        player1 = HumanPlayer("Human", "red")
        player2 = RandomNPC("Computer", "green")
    elif choice == "3":
        player1 = RandomNPC("Bot 1", "red")
        player2 = RandomNPC("Bot 2", "green")
    elif choice == "4":
        agent = agentvV()
        player1 = AgentPlayer("AgentPlayer 1", "red", agent)
        player2 = AgentPlayer( "AgentPlayer 2", "green", agent)
    elif choice == "5":
        agent = AgentMinimax()
        player1 = AgentPlayer("AgentPlayer 1", "red", agent)
        player2 = AgentPlayer( "AgentPlayer 2", "green", agent)
    elif choice == "6":
        agent = AgentMinimax()
        player1 = HumanPlayer("Human", "red")
        player2 = AgentPlayer("AgentPlayer 2", "green", agent)
    elif choice == "7":
        agent = AgentAlphaBeta()
        player1 = AgentPlayer("AgentPlayer 1", "red", agent)
        player2 = AgentPlayer( "AgentPlayer 2", "green", agent)
    elif choice == "8":
        agent = AgentAlphaBeta()
        player1 = HumanPlayer("Human", "red")
        player2 = AgentPlayer("AgentPlayer 2", "green", agent)


    else:
        print("Invalid choice, defaulting to Human vs NPC.")
        player1 = HumanPlayer("Human", "red")
        player2 = RandomNPC("Computer", "green")

    edges = frozenset([(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 7), (5, 8), (6, 7), (7, 8)])
    initial_edges = frozenset([(0, 1), (1, 2), (0, 3), (5, 8), (6, 7), (7, 8)]) #Hier können edges vorbelegt werden. Werden vor dem aufruf des ersten Spielers alle dem ersten Spieler zugewiesen. Keine Punkte vergabe beachtet.

    initial_game_state = GameState(initial_edges, edges-initial_edges, "red", (0, 0), edges)

    # Start the game with the selected players
    game = Game(
        graph_controller=GraphController(grid_size=5),
        player_controller=PlayerController(player1=player1, player2=player2),
        view=GameView()
        , game_state=initial_game_state
    )
    game.start()
