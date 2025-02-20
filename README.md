# PlantProtectionSim (Masterarbeit)

## Einleitung
Dieses Simulationssystem modelliert die Wechselwirkungen zwischen Pflanzen und Fressfeinden unter Berücksichtigung verschiedener pflanzlicher Schutzmechanismen. Das Tool ermöglicht es, eigene Biotope zu erstellen und deren Entwicklung über die Zeit zu simulieren. Dabei werden pflanzliche Kommunikationsmechanismen sowie der Einfluss von Abwehrstoffen visualisiert.

## Funktionen
- Erstellung eines Biotops mit Pflanzen und Fressfeinden
- Simulation der Interaktion zwischen den Akteuren
- Visualisierung des Wachstums und der Populationsdynamik
- Berücksichtigung pflanzlicher Schutzmechanismen (z. B. Giftstoffe, Signalstoffe)
- Anpassbare Parameter für individuelle Simulationen

## Installation
### Voraussetzungen
- Python 3.x
- Paketverwaltung mit `poetry` ([Installationsanleitung](https://python-poetry.org))

### Installationsschritte
1. Repository klonen oder ZIP-Datei herunterladen:
   ```bash
   git clone https://github.com/lucas-diet/PlantProtectionSim.git
   ```
2. In das Projektverzeichnis wechseln:
   ```bash
   cd PlantProtectionSim
   ```
3. Abhängigkeiten installieren:
   ```bash
   poetry install
   ```
4. Anwendung starten:
   ```bash
   poetry run python main.py
   ```

## Nutzung
Es gibt Beispiele im Ordner _files, die importiert werden können.
1. Start des Tools durch Ausführen von `main.py`
2. Im Hauptmenü eine neue Simulation starten oder eine bestehende importieren
3. Parameter für Pflanzen, Fressfeinde und Substanzen festlegen bzw. anpassen
4. Simulation starten und Entwicklungen beobachten
5. Ergebnisse exportieren (Speicherort individuell festlegbar)

## Code-Struktur
- `main.py`: Einstiegspunkt der Anwendung
- `controllers/`
  - `simulation.py`: Enthält die Logik der Simulation
  - `fileManager.py`: Verwaltung von Dateioperationen
- `views/`
  - `gui.py`: Implementiert die graphische Oberfläche
  - `diagrams.py`: Visualisierung der Simulationsergebnisse
- `models/`
  - `plant.py`: Modellklasse für Pflanzen
  - `enemyCluster.py`: Modellklasse für Fressfeind-Cluster
  - `connection.py`: Modellklasse für pflanzliche Verbindungen
  - `signal.py`: Modellklasse für Signalstoffe
  - `substance.py`: Modellklasse für Substanzen
  - `toxin.py`: Modellklasse für Giftstoffe
  - `grid.py`: Modellklasse für das Grid als Biotop


---
Vielen Dank für die Nutzung dieses Simulationssystems!

