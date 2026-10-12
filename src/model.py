
from dataclasses import dataclass
from typing import Tuple, List, Dict

#Klasse für Punkte, die im Spiel verwendet werden. Jeder Punkt hat eine Position und einen Namen.
@dataclass(frozen=True, slots=True)
class Point:
    position: Tuple[int, int]
    name: str

    def __repr__(self) -> str:
        return f"{self.name}({self.position})"

    def __eq__(self, o):
        if self.position[0] == o.position[0] and self.position[1] == o.position[1]:
            return True
        return False
"""
Klasse für Kanten, die zwei Punkte verbinden. Jede Kante hat eine Farbe und einen Status, ob sie ausgewählt ist oder nicht.
Außerdem @properties für Position und Name
"""
@dataclass
class Edge:
    point_one: Point
    point_two: Point
    selected: bool = False
    color: str = ""

    @property
    def position(self) -> Tuple[int, int]:
        p1 = self.point_one.position
        p2 = self.point_two.position
        # Berechne die mittlere Position zwischen den Punkten
        if abs(p1[0] - p2[0]) <= 1:
            # x - Achse
            return (p1[0], min(p1[1], p2[1]) + 1)
        else:
            # Y - Achse
            return (min(p1[0], p2[0]) + 1, p1[1])

    @property
    def name(self) -> str:
        return f"{self.point_one.name} - {self.point_two.name}"

    def select(self, color: str) -> None:
        self.selected = True
        self.color = color

    #Vergleichsmethode
    def __eq__(self, o):
        #print(o, self)
        if self.point_one == o.point_one and self.point_two == o.point_two or self.point_one == o.point_two and self.point_two == o.point_one:
            return True
        return False
    #hash um als Key genutzt zu werden
    def __hash__(self):
        return hash(frozenset((self.point_one, self.point_two)))

@dataclass
class Box:
    edges: [Edge]
    id: int
    color: str= ""
    conquered: bool = False

    @property
    def position(self) -> Tuple[int, int]:
        p1 = self.edges[2].position[0]
        p2 = self.edges[0].position[1]
        return p1, p2



class Graph:
    """
    Eine allgemeine Graph-Klasse, die Knoten und Kanten verwaltet.
    Mit Adjazenzen und Methoden zum Hinzufügen von Knoten und Kanten sowie zum Abrufen aller Kanten.
    """

    def __init__(self) -> None:
        self.adjacency: Dict[Point, List[Edge]] = {}
        self.nodes: List[Point] = []

    def add_node(self, node: Point) -> None:
        self.adjacency.setdefault(node, [])
        self.nodes.append(node)

    # Edge in andere Richtung auskommentiert, da kein Nutzen gesehen und ansonsten nur gestört.
    def add_edge(self, a: Point, b: Point) -> None:
        edge_ab = Edge(a, b)
        #edge_ba = Edge(b, a)
        self.adjacency[a].append(edge_ab)
        #self.adjacency[b].append(edge_ba)

    def get_edges(self) -> List[Edge]:
        edge_list = []
        for ed_list in self.adjacency.values():
            for edge in ed_list:
                edge_list.append(edge)
        return edge_list

    #Wie der Graph ausgegeben wird, z.B. für Debugging-Zwecke
    def __repr__(self) -> str:
        out = "Graph adjacency list:\n"
        for node, edges in self.adjacency.items():
            edge_names = [edge.name for edge in edges]
            out += f"{node.name}: {edge_names}\n"
        return out
