

import os  
os.system('clear')

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from collections import Counter

from customTestResults import CustomTestRunner
from models.grid import Grid
from models.plant import Plant
from models.enemyCluster import Enemy, EnemyCluster

# === Konstanten ===
PLANT_COLORS = [
    '#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57',
    '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98',
    '#9ACD32', '#6B8E23'
]

class TestsCluster(unittest.TestCase):
    # ---- Setup-Methode ----
    def setUp(self):
        # Initialisiere Grid, Feinde und Standardwerte für die Tests.
        self.grid = Grid(width=6, height=6)
        
        # Initialisiere Feinde
        self.enemy1 = Enemy(name='e1', symbol='E1')
        self.enemy2 = Enemy(name='e2', symbol='E2')
        self.enemy3 = Enemy(name='e3', symbol='E3')

    # ---- Tests ----
    def test_enemy_moves_to_closest_plant(self):
        p1 = Plant(name='p1', initEnergy=300, growthRateEnegry=1, minEnegrgy=50,
              reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
              position=(3, 1), grid=self.grid, color=PLANT_COLORS)
        p2 = Plant(name='p2', initEnergy=100, growthRateEnegry=2, minEnegrgy=50,
              reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
              position=(3, 4), grid=self.grid, color=PLANT_COLORS)
        p3 = Plant(name='p3', initEnergy=100, growthRateEnegry=1, minEnegrgy=50,
              reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2,
              position=(5, 0), grid=self.grid, color=PLANT_COLORS)

        ec1 = EnemyCluster(enemy=self.enemy1, num=2, speed=1, position=(2, 0), grid=self.grid, eatingSpeed=5, eatVictory=10)
        ec2 = EnemyCluster(enemy=self.enemy2, num=2, speed=1, position=(2, 0), grid=self.grid, eatingSpeed=10, eatVictory=10)
        ec3 = EnemyCluster(enemy=self.enemy3, num=1, speed=1, position=(0, 4), grid=self.grid, eatingSpeed=10, eatVictory=10)
        
        plants = [p1, p2, p3]
        enemies = [ec1, ec2, ec3]

        for plant in plants: self.grid.addPlant(plant)
        for ec in enemies: self.grid.addEnemies(ec)

        # Erwartete Zielpflanzen
        expected_targets = {
            enemies[0]: (3, 1),  # e1
            enemies[1]: (3, 1),  # e2
            enemies[2]: (3, 4)   # e3
        }

        for ec, expected_target in expected_targets.items():
            path = ec.getPath(ec.position)
            self.assertEqual(ec.targetPlant, expected_target, f'{ec.enemy.name} hat das falsche Ziel!')
            self.assertTrue(path, f'{ec.enemy.name} hat keinen gültigen Pfad!')

    
    def test_choose_random_plant_with_equal_distance(self):

        # Initialisiere Feindcluster
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(2, 2), grid=self.grid, eatingSpeed=5, eatVictory=10)

        # Definiere Pflanzen in gleicher Entfernung
        p1 = Plant(name='p1', initEnergy=300, growthRateEnegry=1, minEnegrgy=50, reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2, position=(0, 0), grid=self.grid, color=PLANT_COLORS)
        p2 = Plant(name='p2', initEnergy=300, growthRateEnegry=1, minEnegrgy=50, reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2, position=(0, 4), grid=self.grid, color=PLANT_COLORS)
        p3 = Plant(name='p3', initEnergy=300, growthRateEnegry=1, minEnegrgy=50, reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2, position=(4, 0), grid=self.grid, color=PLANT_COLORS)
        p4 = Plant(name='p4', initEnergy=300, growthRateEnegry=1, minEnegrgy=50, reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2, position=(4, 4), grid=self.grid, color=PLANT_COLORS)

        plants = [p1, p2, p3, p4]

        for plant in plants: self.grid.addPlant(plant)
        self.grid.addEnemies(ec)

        # Liste der möglichen Ziele
        possible_targets = [p1.position, p2.position, p3.position, p4.position]
        target_counts = {p1.position: 0, p2.position: 0, p3.position: 0, p4.position: 0}

        # Simuliere mehrfaches Wählen einer Pflanze
        for _ in range(100):  # Wiederholte Tests für Zufälligkeit
            ec.targetPlant = None  # Reset Ziel
            chosen_path = ec.chooseRandomPlant(start=ec.position)
            chosen_target = chosen_path[-1] if chosen_path else None
            self.assertIn(chosen_target, possible_targets, 'Die gewählte Pflanze ist nicht in den möglichen Zielen')
            target_counts[chosen_target] += 1

        # Prüfe, dass jede Pflanze mindestens einmal ausgewählt wurde
        for target, count in target_counts.items():
            self.assertGreater(count, 0, f'Die Pflanze {target} wurde nie ausgewählt')

    
    def test_enemy_movement_horizontal_vertical(self):
        #"""Prüft, ob Feinde waagerecht und senkrecht laufen können."""
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(0, 0), grid=self.grid, eatingSpeed=5, eatVictory=10)
        self.grid.addEnemies(ec)

        target_position = (4, 4)
        path = ec.findShortestPath(start=ec.position, goal=target_position)

        # Erwarteter Pfad
        expected_path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4)]
        self.assertEqual(path, expected_path, 'Der Pfad entspricht nicht den Erwartungen!')

    
    def test_chooseRandomPlant_no_plants(self):
        # Testen, wenn es keine Pflanzen im Grid gibt
        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(0, 0), grid=self.grid, eatingSpeed=5, eatVictory=10)
        self.grid.addEnemies(ec)

        result = ec.chooseRandomPlant((3, 3))
        self.assertEqual(result, [], 'Es sollte keine Pflanzen im Grid sein.')
    

    def test_chooseRandomPlant_one_plant(self):
        # Testen, wenn es genau eine Pflanze gibt
        p1 = Plant(name='p1', initEnergy=300, growthRateEnegry=1, minEnegrgy=50, reproductionIntervall=0, offspingEnergy=60, minDist=1, maxDist=2, position=(3, 3), grid=self.grid, color=PLANT_COLORS)
        self.grid.addPlant(p1)

        ec = EnemyCluster(enemy=self.enemy1, num=1, speed=1, position=(0, 0), grid=self.grid, eatingSpeed=5, eatVictory=10)
        self.grid.addEnemies(ec)

        result = ec.chooseRandomPlant((0, 0))

        # Überprüfen, ob der Pfad nur zum Ziel führt, ohne unzulässige Wege zu nutzen
        valid_paths = [
            [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3)],  # direkter Pfad
            [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]   # direkter Pfad
        ]

        self.assertIn(result, valid_paths, 'Es sollte nur einen direkten Pfad zur einzigen Pflanze geben und nicht auf andere unzulässige Pfade ausweichen.')

        # Überprüfen, ob der gewählte Pfad keinen unzulässigen Weg enthält
        disallowed_paths = [
            [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)],
            [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)], 
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 3)],  
            [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (3, 3)], 
        ]

        self.assertNotIn(result, disallowed_paths, 'Der gewählte Pfad sollte keinen unzulässigen Pfad enthalten.')


    def test_enemy_eats_plant(self):
        # Prüft, ob Feinde Pflanzen fressen und die Energie korrekt reduziert wird.
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
        self.assertEqual(plant.currEnergy, expected_energy, 'Die Energie der Pflanze wurde nicht korrekt reduziert.')
        if plant.currEnergy <= plant.minEnergy:
            self.assertNotIn(plant, self.grid.plants, 'Die Pflanze sollte entfernt worden sein.')
        else:
            self.assertIn(plant, self.grid.plants, 'Die Pflanze sollte noch existieren.')


    def test_enemy_reproduction(self):
        # Prüft, ob ein Feind sich vermehrt, wenn er genug Energie gegessen hat.
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

# === Main-Methode ===
if __name__ == '__main__':
    runner = CustomTestRunner()
    unittest.main(testRunner=runner)