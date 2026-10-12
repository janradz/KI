from dataclasses import dataclass
import random

from Agents.agent import Agent
from State.problem import GameState


#abstrakte klasse für spieler
@dataclass
class Player():
    name: str
    color: str
    #NEW
    points: int = 0
    def get_move(self, game_state: GameState) -> tuple[int, int]:
        pass

#bisherige player klasse
class HumanPlayer(Player):
    def get_move(self,game_state: GameState) -> tuple[int,int]:
        print(f"Select Point for {self.name} from 0 to 8: ")
        while True:
            try:
                point1 = int(input("Point1 := "))
                point2 = int(input("Point2 := "))

                if point1 < 0 or point1 > 8 or point2 < 0 or point2 > 8:
                    print("Ungültige Eingabe: Die Punkte müssen zwischen 0 und 8 liegen. Bitte versuche es erneut.")
                    continue # Springt wieder an den Anfang der while-Schleife
                
                # NEU: Verhindern, dass ein Punkt mit sich selbst verbunden wird (z.B. 0-0)
                if point1 == point2:
                    print("Ungültige Eingabe: Du musst zwei verschiedene Punkte wählen.")
                    continue
    
                return point1, point2
            except ValueError:
                print("Invalid Input")
    
#NEUE npc klasse
class RandomNPC(Player):
    def get_move(self, game_state: GameState) -> tuple[int,int]:
        print(f"{self.name} (NPC) is thinking..")
        
        #random auswahl von moves
        move = random.choice(game_state.not_drawn_edges)
        print(f"{self.name} chose {move[0]} - {move[1]}")
        
        return move


class AgentPlayer(Player):
    def __init__(self, name: str, color: str, agent: Agent):
        super().__init__(name, color)
        self.agent = agent
    def get_move(self, game_state: GameState) -> tuple:

        return self.agent.get_move(game_state)