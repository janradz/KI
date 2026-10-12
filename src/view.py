

from typing import List
from termcolor import colored


class GameView:
    """
    Verwaltet die Darstellung des Spiels (Grid-Ansicht).
    """
    """Funktion, die ein 2D-Array erstellt, um das Spielfeld darzustellen. Es füllt die Array mit "*" für Punkte und " " für leere Felder."""
    def __create_print_array(self, grid_size: int) -> List[List[str]]:

       array = []
       for i in range(grid_size):
           row = []
           for j in range(grid_size):
               row.append("*" if (i % 2 == 0 and j % 2 == 0) else " ")
           array.append(row)
       return array
    """Funktion, die das 2D-Array basierend auf den ausgewählten Kanten aktualisiert. Es ersetzt die entsprechenden Positionen im Array mit Linien ("-" für horizontal und "|" für vertikal) und färbt sie entsprechend der Farbe der Kante."""
    def __update_print_array(self, graph: dict) -> None:

       for point, edges in graph.items():
           for edge in edges:
               if edge.selected:
                   pos = edge.position
                   i, j = int(pos[0]), int(pos[1])
                   # Unterscheide horizontal und vertikal.
                   if edge.point_one.position[0] == edge.point_two.position[0]:
                       self.print_array[i][j] = colored(u'\u2500', edge.color)
                   else:
                       self.print_array[i][j] = colored("|", edge.color)
    """Funktion, die das 2D-Array ausgibt. Es iteriert durch jede Zeile des Arrays und druckt sie als String aus, um die aktuelle Darstellung des Spielfelds anzuzeigen."""
    def display(self, grid_size: int, graph: dict,  boxes: dict) -> None:
       self.print_array = self.__create_print_array(grid_size)
       self.__update_print_array(graph)
      # Schleife 1: Setzt die Symbole in die Boxen (iteriert 4 mal)
       for b_id, box in boxes.items():
           if box.conquered:
               i, j = box.position
               
               if box.color == "red":
                   symbol = u'\u25B2'  # ▲ (Dreieck für P1)
               else:
                   symbol = u'\u25A0'  # ■ (Viereck für P2 / NPC)
                   
               self.print_array[i][j] = colored(symbol, box.color)

       # Schleife 2: Druckt das Spielfeld (darf NICHT in Schleife 1 eingerückt sein!)
       for row in self.print_array:
           print("".join(row))
