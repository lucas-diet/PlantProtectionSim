
import os  
os.system('clear')


import unittest
import random
from models.grid import Grid  # Importiere deine Grid-Klasse (Anpassen an deinen Kontext)
from models.enemy import Enemy # Importiere Feindklassen
from models.enemyCluster import EnemyCluster 
from models.plant import Plant  # Importiere Pflanzenklasse
from models.signal import Signal
from models.substance import Substance

import unittest
from io import StringIO

# === Konstanten ===
PLANT_COLORS = [
    '#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57',
    '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98',
    '#9ACD32', '#6B8E23'
]

class CustomTestResult(unittest.TextTestResult):
    
    def startTest(self, test):
        super().startTest(test)
        self.stream.write(f"\nStarte Test: {test._testMethodName}\n")
        self.stream.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"[✔] Erfolgreich: {test._testMethodName}\n\n")
        self.stream.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"[✘] Fehler: {test._testMethodName}\n")
        self.stream.write(f"    Grund: {self._exc_info_to_string(err, test)}\n\n")
        self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"[⚠] Fehler: {test._testMethodName}\n")
        self.stream.write(f"    Grund: {self._exc_info_to_string(err, test)}\n\n")
        self.stream.flush()

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.stream.write(f"[⏩] Übersprungen: {test._testMethodName} - Grund: {reason}\n\n")
        self.stream.flush()

class CustomTestRunner(unittest.TextTestRunner):
    """Angepasster TestRunner für bessere Formatierung mit Leerzeilen zwischen den Tests."""
    resultclass = CustomTestResult

    def __init__(self, *args, **kwargs):
        kwargs['verbosity'] = 2  # Setze Standard-Verbosity auf 2
        super().__init__(*args, **kwargs)


# === Testklasse ===
class Tests(unittest.TestCase):

    # ---- Setup-Methode ----
    def setUp(self):
        """Initialisiere Grid, Feinde und Standardwerte für die Tests."""
        self.grid = Grid(width=6, height=6)
        
        # Initialisiere Feinde
        self.enemy1 = Enemy(name='e1', symbol='E1')
        self.enemy2 = Enemy(name='e2', symbol='E2')
        self.enemy3 = Enemy(name='e3', symbol='E3')

        s1 = Substance(name='s1', type='signal')

    # ---- Hilfsfunktionen ----
    def add_plants_and_enemies(self):
        """Füge Standardpflanzen und Feinde zum Grid hinzu (für Testzwecke)."""
        plants = [
            Plant(name='p1', initEnergy=300, growthRateEnegry=1, minEnegrgy=50,
                  reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
                  position=(3, 1), grid=self.grid, color=PLANT_COLORS),
            Plant(name='p2', initEnergy=100, growthRateEnegry=2, minEnegrgy=50,
                  reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
                  position=(3, 4), grid=self.grid, color=PLANT_COLORS),
            Plant(name='p3', initEnergy=100, growthRateEnegry=1, minEnegrgy=50,
                  reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
                  position=(5, 0), grid=self.grid, color=PLANT_COLORS)
        ]
        for plant in plants:
            self.grid.addPlant(plant)

        enemies = [
            EnemyCluster(enemy=self.enemy1, num=2, speed=1, position=(2, 0), grid=self.grid, eatingSpeed=5, eatVictory=10),
            EnemyCluster(enemy=self.enemy2, num=2, speed=1, position=(2, 0), grid=self.grid, eatingSpeed=10, eatVictory=10),
            EnemyCluster(enemy=self.enemy3, num=1, speed=1, position=(0, 4), grid=self.grid, eatingSpeed=10, eatVictory=10)
        ]
        for enemy in enemies:
            self.grid.addEnemies(enemy)


    # ---- Tests ----
    def test_enemy_moves_to_closest_plant(self):
        self.add_plants_and_enemies()

        # Erwartete Zielpflanzen
        expected_targets = {
            self.grid.enemies[0]: (3, 1),  # e1
            self.grid.enemies[1]: (3, 1),  # e2
            self.grid.enemies[2]: (3, 4)   # e3
        }

        for ec, expected_target in expected_targets.items():
            path = ec.getPath(ec.position)
            self.assertEqual(ec.targetPlant, expected_target, f"{ec.enemy.name} hat das falsche Ziel!")
            self.assertTrue(path, f"{ec.enemy.name} hat keinen gültigen Pfad!")


    def test_enemy_eats_plant(self):
        #"""Prüft, ob Feinde Pflanzen fressen und die Energie korrekt reduziert wird."""
        plant = Plant(name='p1', initEnergy=50, growthRateEnegry=1, minEnegrgy=10,
                      reproductionIntervall=0, offspingEnergy=20, minDist=1, maxDist=2,
                      position=(2, 2), grid=self.grid, color=PLANT_COLORS)
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(2, 2), grid=self.grid, eatingSpeed=10, eatVictory=10)

        # Hinzufügen zum Grid
        self.grid.addPlant(plant)
        self.grid.addEnemies(ec)

        # Vorheriger Energielevel
        initial_energy = plant.currEnergy

        # Fressen simulieren
        ec.eatPlant(ec, plant)

        # Erwartungen prüfen
        expected_energy = initial_energy - ec.eatingSpeed
        self.assertEqual(plant.currEnergy, expected_energy, "Die Energie der Pflanze wurde nicht korrekt reduziert.")
        if plant.currEnergy <= plant.minEnergy:
            self.assertNotIn(plant, self.grid.plants, "Die Pflanze sollte entfernt worden sein.")
        else:
            self.assertIn(plant, self.grid.plants, "Die Pflanze sollte noch existieren.")


    def test_enemy_movement_horizontal_vertical(self):
        #"""Prüft, ob Feinde waagerecht und senkrecht laufen können."""
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(0, 0), grid=self.grid, eatingSpeed=5, eatVictory=10)
        self.grid.addEnemies(ec)

        target_position = (4, 4)
        path = ec.findShortestPath(start=ec.position, goal=target_position)

        # Erwarteter Pfad
        expected_path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4)]
        self.assertEqual(path, expected_path, "Der Pfad entspricht nicht den Erwartungen!")
    

    def test_enemy_reproduction(self):
        #"""Prüft, ob ein Feind sich vermehrt, wenn er genug Energie gegessen hat."""
        # Initialisiere Feindcluster
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(0, 0), grid=self.grid, eatingSpeed=10, eatVictory=20)
        
        # Füge Feind zum Grid hinzu
        self.grid.addEnemies(ec)
        
        # Simuliere, dass der Feind genug Energie gegessen hat
        ec.eatedEnergy = 60  # Genug Energie für 3 neue Feinde (60 / 20 = 3)
        
        # Rufe die reproduce-Methode auf
        ec.reproduce()
        
        # Erwartete Anzahl neuer Feinde
        expected_num = 1 + 3  # Startanzahl + 3 neue Feinde
        expected_energy = 60 - (3 * 20)  # Restenergie nach Reproduktion
        
        # Assertions: Anzahl Feinde und verbleibende Energie prüfen
        self.assertEqual(ec.num, expected_num, f"Die Anzahl der Feinde sollte {expected_num} sein, ist aber {ec.num}.")
        self.assertEqual(ec.eatedEnergy, expected_energy, f"Die Restenergie sollte {expected_energy} sein, ist aber {ec.eatedEnergy}.")
        self.assertEqual(ec.newBorns, 0, "Die Anzahl neuer Feinde (newBorns) sollte nach Reproduktion 0 sein.")

    def test_signal_creation(self):
        self.add_plants_and_enemies()
        
        # Definition des Signals
        s1 = Substance(name='s1', type='signal')
        sig1 = Signal(
            substance=s1,
            emit=[self.grid.plants[0], self.grid.plants[1]],  # Die Pflanzen, die das Signal aussenden
            receive=[self.grid.plants[2]],  # Die Pflanzen, die das Signal empfangen können
            triggerCombination=[[self.enemy1, 2]],  # Kombinationen, die das Signal auslösen
            prodTime=3,  # Produktionszeit des Signals
            spreadType='symbiotic',  # Art der Ausbreitung
            sendingSpeed=2,  # Geschwindigkeit des Signal-Ausstoßes
            energyCosts=3,  # Energieaufwand für das Signal
            afterEffectTime=2,  # Dauer der Wirkung nach Empfang
            spreadSpeed=None  # Geschwindigkeit der Ausbreitung (optional)
        )

        # Überprüfe, ob das Signal korrekt erstellt wurde
        self.assertEqual(sig1.substance.name, 's1', "Der Substanzname des Signals stimmt nicht überein.")
        self.assertEqual(sig1.substance.type, 'signal', "Der Substanztyp des Signals stimmt nicht überein.")
        self.assertEqual(sig1.emit, [self.grid.plants[0], self.grid.plants[1]], "Die Emit-Pflanzen sind nicht korrekt.")
        self.assertEqual(sig1.receive, [self.grid.plants[2]], "Die Empfang-Pflanze ist nicht korrekt.")
        self.assertEqual(sig1.triggerCombination, [[self.enemy1, 2]], "Die Triggerkombination ist nicht korrekt.")
        self.assertEqual(sig1.prodTime, 3, "Die Produktionszeit ist nicht korrekt.")
        self.assertEqual(sig1.spreadType, 'symbiotic', "Die Ausbreitungsart ist nicht korrekt.")
        self.assertEqual(sig1.sendingSpeed, 2, "Die Sendegeschwindigkeit ist nicht korrekt.")
        self.assertEqual(sig1.energyCosts, 3, "Die Energiekosten sind nicht korrekt.")
        self.assertEqual(sig1.afterEffectTime, 2, "Die Nachwirkungenzeit ist nicht korrekt.")



# === Main-Methode ===
if __name__ == '__main__':
    runner = CustomTestRunner()
    unittest.main(testRunner=runner)
