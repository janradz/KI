# Ausführen und testen

## Installation

Empfohlen: eine virtuelle Python-Umgebung. Syntax, Suchtests und die A*-Konsolendemo wurden mit Python 3.12.9 geprüft. Die vollständige Abhängigkeitskombination und das neuronale Training wurden bei diesem Import nicht neu getestet; die Requirements sind noch kein reproduzierbar fixierter Lockfile.

```sh
python -m venv .venv
```

Aktivierung unter Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Unter Linux/macOS:

```sh
source .venv/bin/activate
```

Anschließend:

```sh
python -m pip install -r requirements.txt
```

Für die Bildklassifikation zusätzlich:

```sh
python -m pip install -r requirements-ml.txt
```

Die optionale Labyrinth-Oberfläche benötigt Tkinter und eine grafische Desktop-Sitzung. Tkinter wird je nach Python-Distribution beziehungsweise Betriebssystem separat mitgeliefert oder installiert.

## Ausführen

Alle folgenden Befehle beginnen im Repository-Hauptverzeichnis.

**A*-Konsolendemo** – benötigt nur die Python-Standardbibliothek:

```sh
cd src/labyrinth
python controller.py
```

Im selben Verzeichnis startet `python ui.py` die optionale Oberfläche. Deren Autorenhinweis ist im Quellcode und in `CREDITS.md` erhalten.

**Dots and Boxes:**

```sh
python src/controller.py
```

Die Konsole bietet unterschiedliche Spieler-/Agentenkombinationen. Der ursprüngliche Spielcode besitzt noch bekannte Einschränkungen; siehe unten.

**Aussagenlogik:**

```sh
cd src
python -m logicparser.aufgabe20
```

**Fashion-MNIST:**

```sh
cd src/pytorch
python "aufgabe 23.py"
```

Beim ersten Start lädt torchvision die Trainings- und Testdaten herunter. Der Lauf trainiert mehrere Modelle und kann entsprechend dauern. Die Ergebnisse hängen vom Lauf ab; es werden keine fest zugesicherten Genauigkeiten behauptet.

## Tests und bekannte Grenzen

Suchtests unter PowerShell, aus dem Repository-Hauptverzeichnis:

```powershell
$env:PYTHONPATH = "$PWD/src"
python -B -m unittest discover -s tests -p test_search.py -v
```

Unter Linux/macOS:

```sh
PYTHONPATH=src python -B -m unittest discover -s tests -p test_search.py -v
```

Beim Import am 08.10.2026 bestanden alle vier Suchtests. Sie prüfen verfügbare Züge, Spielerwechsel, Punktevergabe und die Rückgabe eines Plans zum Zielzustand. Die vollständige Suche kann einige Zeit dauern.

- `tests/test_game.py` enthält ältere Tests, deren Aufrufe nicht mehr zur aktuellen `Game`-Schnittstelle passen. Diese Tests sind nicht als bestanden ausgewiesen.
- Der Zufallsspieler verwendet derzeit `random.choice` auf einem `frozenset`; die NPC-Modi benötigen eine Korrektur, bevor sie zuverlässig nutzbar sind.
- GUI, Aussagenlogik und vollständiges PyTorch-Training wurden bei diesem Import nicht ausgeführt.
- Die PyTorch-Skripte starten Daten-Download und Training auf Modulebene. Sie sind als direkt gestartete Lernskripte zu verstehen, nicht als nebenwirkungsfreie Bibliotheksmodule.
- `aufgabe22.py` gibt Trainingsgenauigkeit aus. `aufgabe 23.py` enthält zusätzlich eine Auswertung mit Testdaten. Diese Werte sind zu unterscheiden.

## Daten und Herkunft

Fashion-MNIST stammt von [Zalando Research](https://github.com/zalandoresearch/fashion-mnist) und wird über torchvision bezogen. Die Daten sind nicht im Repository enthalten.

Autorenhinweise und Grenzen der Zuordnung: [CREDITS.md](CREDITS.md).
