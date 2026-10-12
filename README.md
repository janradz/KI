# AI Search and Learning

Python-Projekte aus dem KI-Praktikum an der FH Münster: Spielsuche, A*-Pfadsuche, Aussagenlogik und Bildklassifikation.

**Hochschul-Teamprojekt · Python · PyTorch · NLTK**

## Teilprojekte

| Projekt | Inhalt |
|---|---|
| Labyrinth | A* mit Manhattan-Heuristik, Feldkosten und Pfadrekonstruktion |
| Dots and Boxes | Spielmodell, Uniform-Cost-Suche, Minimax und Alpha-Beta |
| Aussagenlogik | Wissensbasis, Formelauswertung und Inferenz mit NLTK |
| Fashion-MNIST | Neuronale Netze zum Klassifizieren von Kleidungsbildern |

## Eigener Beitrag

Schwerpunkte: A*-Pfadsuche mit Pfadrekonstruktion sowie PyTorch-Implementierungen für Fashion-MNIST mit unterschiedlichen Netzarchitekturen, Training und Auswertung. Weitere Beiträge betreffen das Spielmodell, die Suchlogik und die Logikaufgaben.

Das Projekt entstand im Sommersemester 2026 als Teamarbeit auf Basis von Hochschulvorlagen. Die Zuordnung der Beiträge und übernommener Bestandteile steht in [CREDITS.md](CREDITS.md).

## Ausführung: A*-Pfadsuche

Die Konsolendemo benötigt nur Python und die Standardbibliothek. Geprüft wurde sie beim Import mit Python 3.12.9.

```sh
cd src/labyrinth
python controller.py
```

Für Bildklassifikation und die übrigen Teilprojekte gibt es eine [Anleitung zu Installation, Ausführung und Tests](RUNNING.md). Fashion-MNIST wird beim ersten Training über torchvision heruntergeladen.

## Aktueller Stand

Beim Import am 8. Oktober 2026 bestanden die vier Suchtests; die A*-Konsolendemo wurde ebenfalls geprüft. GUI, Aussagenlogik und vollständiges PyTorch-Training wurden dabei nicht erneut ausgeführt.

Im Spielprojekt sind noch Fehler offen: Der Zufallsspieler verwendet `random.choice` auf einem `frozenset`, und ältere Spieltests passen nicht mehr zur aktuellen Schnittstelle. Einzelheiten stehen in [RUNNING.md](RUNNING.md#tests-und-bekannte-grenzen).

## Herkunft

Die GitHub-Version wurde am 8. Oktober 2026 aus einem ZIP-Snapshot importiert. Die ursprüngliche GitLab-Historie ist nicht enthalten. Aufgabenblätter und heruntergeladene Datensätze sind nicht Teil des Repositories.

Fashion-MNIST stammt von [Zalando Research](https://github.com/zalandoresearch/fashion-mnist). Autorenhinweise und Grundlagen der Beitragszuordnung: [CREDITS.md](CREDITS.md).
