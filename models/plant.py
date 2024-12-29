

import random
import numpy as np

class Plant():

    def __init__(self, name, initEnergy, growthRateEnegry, minEnegrgy, reproductionIntervall, offspingEnergy, minDist, maxDist, position, grid, color):
        self.name = name
        self.initEnergy = initEnergy
        self.currEnergy = initEnergy
        self.growthRateEnegry = growthRateEnegry
        self.minEnergy = minEnegrgy
        self.reproductionIntervall = reproductionIntervall
        self.offspringEnergy = offspingEnergy
        self.minDist = minDist
        self.maxDist = maxDist
        self.position = position
        self.grid = grid
        self.color = color[int(self.name[1])-1]
        
        self.age = 0
        self.gridConnections = {}

        self.signalAlarms = {}
        self.isSignalSignaling = {}

        self.signalProdCounters = {}
        self.signalSendingCounters = {}
        #self.afterEffectTime = 0
        self.afterEffectTimes = {}

        self.toxinAlarms = {}
        self.isToxically = {}

        self.toxinProdCounters = {} #dict, wo produktionsCounter für jedes [ec, toxin] gespeichert wird.
        self.airSpreadCounters = {}

    def grow(self):
        """_summary_
            Aktualisiert die aktuelle Energie der Pflanze basierend auf dem Anfangswert und dem Wachstumsfaktor. 
            Der Wachstumsfaktor gibt an, um wie viel Prozent die Energie jedes Mal zunimmt. 
            Die Methode fügt zudem 1 zum Alter des Objekts hinzu.
        """
        self.currEnergy += self.initEnergy * (self.growthRateEnegry / 100)
        self.age += 1


    def survive(self):
        """_summary_
            Überprüft, ob die Pflanze genug Energie zur Verfügung hat, um zu überleben. 
            Wenn die aktuelle Energie unter dem Mindestwert liegt, wird die Pflanze aus dem Grid entfernt.
        """
        if self.currEnergy < self.minEnergy:
            self.grid.removePlant(self)
            
        
    def scatterSeed(self):
        """_summary_
            Überprüft, ob die Pflanze bereit ist, Samen zu verstreuen, basierend auf ihrem Alter und dem Reproduktionsintervall. 
            Wenn die Bedingung erfüllt ist, erzeugt die Methode zufällig zwischen 1 und 4 Nachkommen. 
            Für jedes Nachkommen wird die anfängliche Energie abgefragt, und es wird ein neues Pflanzenobjekt erstellt. 
            Die Position jedes Nachkommens wird mittels 'setOffspringPos()' ermittelt, und das Nachkommen wird dem Grid hinzugefügt.
        """
        if self.reproductionIntervall == 0:
            pass

        elif self.age % self.reproductionIntervall == 0:
            for _ in range(random.randint(1, 4)):       ## Zufall zwischen 1 und 4              # Wie viele Kinder soll es max geben?
                offspringPosition = self.setOffspringPos()
                
                if offspringPosition:
                    energyInput = input('Init-Energy of offspring:')                        # Input() famit Energie für jedes Nachkommen individuell ist
                    offspringEnergy = float(energyInput) if energyInput else 100            # default ist 100 Einheiten
                    offspring = Plant(name=self.name, 
                                      initEnergy=self.offspringEnergy, 
                                      growthRateEnegry=self.growthRateEnegry, 
                                      minEnegrgy=self.minEnergy, 
                                      reproductionIntervall=self.reproductionIntervall, 
                                      offspingEnergy=offspringEnergy,
                                      minDist=self.minDist, 
                                      maxDist=self.maxDist, 
                                      position=offspringPosition, 
                                      grid=self.grid,
                                      color=self.color
                    )
                    self.grid.addPlant(offspring)
    

    def setOffspringPos(self):
        """_summary_
            Bestimmt eine geeignete Position für das Erzeugen von Nachkommen innerhalb des Grids. 
            Die Methode überprüft alle möglichen Richtungen rund um die aktuelle Position der Pflanze. 
            Zufällig angeordnete Bewegungsrichtungen werden genutzt, um neue Positionen zu testen. 
            Jede getestete Position wird auf ihre Gültigkeit überprüft: ob sie innerhalb der Gittergrenzen liegt und ob sie frei ist (nicht von einer anderen Pflanze belegt). 
            Falls eine geeignete Position gefunden wird, wird diese zurückgegeben. Andernfalls wird "None" zurückgegeben.
        Returns:
            tuple oder None: Eine gültige Position für das Erzeugen eines Nachkommens oder 'None', wenn keine geeignete Position gefunden wird.
        """
        directions = self.getDirections()
        random.shuffle(directions)

        for dx, dy in directions:
            newX, newY = self.position[0] + dx, self.position[1] + dy
            
            if self.grid.isWithinBounds(newX, newY):
                if not self.grid.isOccupied((newX, newY)):
                    print(f'[DEBUG]: {self.name} auf {self.position} erzeugt Nachkommen auf {newX, newY}')
                    return (newX, newY)
                else:
                    print(f'[DEGUB]: Position {newX, newY} ist belegt. Nachkomme wird nicht erzeugt.')
                    pass
            else:
                print(f'[DEBUG]: Position {newX, newY} liegt außerhalb der Grenzen.')
                pass
            
        return None


    def getDirections(self):
        """_summary_
            Generiert alle möglichen Bewegungsrichtungen innerhalb eines bestimmten Entfernungsbereichs von der aktuellen Position der Pflanze. 
            Die Methode erzeugt Richtungen als Paare von Änderungen in den x- und y-Koordinaten ('dx', 'dy'), die innerhalb des maximalen und minimalen zulässigen Abstandes liegen. 
            Jede Richtung wird durch ihre relativen Differenzen in x- und y-Richtung angegeben. 
        Returns:
            list: Eine Liste von Tupeln, die alle möglichen Richtungen innerhalb des erlaubten Entfernungsbereichs darstellen.
        """
        directions = []
        for dx in range(-self.maxDist, self.maxDist+1):
            for dy in range(-self.maxDist, self.maxDist+1):
                dist = int(np.sqrt(dx**2 + dy**2))
                if self.minDist <= dist <= self.maxDist:
                    directions.append((dx, dy))
        
        return directions


    def getColor(self):
        """_summary_
            Gibt die aktuelle Farbe der Pflanze zurück.
        Returns:
            str: Der Farbwert der Pflanze in Hexadezimalcode.
        """
        return self.color

    
    def resetSignalProdCounter(self, ec, signal):
        """_summary_
            Setzt den Zähler für die Produktion von Signalen auf 0 für eine gegebens Fressfeindcluster und ein spezifisches Signal. 
            Dies wird verwendet, um die Zählung von erzeugten Signalen zurückzusetzen.
        Args:
            ec (Objekt): Ein Obejkt der Klasse EnemyCluster
            signal (Objekt): Ein Obejkt der Klasse Signal

        """
        self.signalProdCounters[ec, signal] = 0


    def incrementSignalProdCounter(self, ec, signal):
        """_summary_
            Erhöht den Zähler für die Produktion von Signalen um 1 für eine gegebene Objekt der Klasse EnemyClsuer und ein Objekt der Klasse Signal. 
            Falls der Zähler für die gegebene Kombination von EnemyClsuer und Signal noch nicht existiert, wird dieser erstellt und auf 1 initialisiert.
        Args:
            ec (Objekt): Ein Obejkt der Klasse EnemyCluster, für die der Signalzähler erhöht werden soll.
            signal (Objekt): Ein Obejkt der Klasse Signal, für das der Zähler erhöht wird.

        """
        key = (ec, signal)
        if key in self.signalProdCounters:
            self.signalProdCounters[ec, signal] += 1
        else:
            self.signalProdCounters[ec, signal] = 1


    def getSignalProdCounter(self, ec, signal):
        """_summary_
            Holt den Zähler für die Produktion von Signalen für ein Kombination aus EnemyCluster und Signal. 
            Wenn der Zähler für die gegebene Kombination von EnemyCluster und Signal nicht existiert, wird ein Standardwert von 1 zurückgegeben.
        Args:
            ec (EnemyCluster): Die Klasse EnemyCluster, die als Objekt.
            signal (Signal): Die Klasse Signal, die als Objekt übergeben wird und für die der Zähler erhöht wird
        Returns:
           int: Der Zähler für die gegebene Signalproduktion in der angegebenen EnemyCluster Klasse, oder 1, wenn der Zähler nicht existiert.
        """
        key = (ec, signal)
        return self.signalProdCounters.get(key, 1)
    

    def resetSignalSendCounter(self, ec, signal, rPlant):
        """_summary_
            Setzt den Zähler für das Senden von Signalen auf 0 für ein gegebenes Objekt EnemyCluster, 
            ein Objekt von einem Signal und einen bestimmten Empfänger ('rPlant') als Objekt der Klasse Plant. 
            Diese Methode wird verwendet, um den Sende-Counter der eines gesendeteten Signals zurückzusetzen,
            die von einer Pflanze an einen bestimmten Empfänger gesendet wurden.
        Args:
            ec (EnemyCluster): Ein Objekt der Klasse EnemyCluster.
            signal (Signal): Ein Objekt der Klasse Signal
            rPlant (Plant): Der spezifische Empfänger, als Objekt der Klasse Plant.
        """
        self.signalSendingCounters[ec, signal, rPlant] = 0


    def incrementSignalSendCounter(self, ec, signal, rPlant):
        """_summary_
            Erhöht den Zähler für das Senden von Signalen um 1 für eine gegebenes EnemyCluster, 
            ein spezifisches Signal und einen bestimmten Empfängerpflanze. 
            Falls der Zähler für die gegebene Kombination von EnemyCluster, 
            Signal und Empfängerpflanze noch nicht existiert, wird dieser erstellt und auf 1 initialisiert.
        Args:
            ec (EnemyCluster): Ein Objekt der Klasse EnemyCluster.
            signal (Signal): Ein Objekt der Klasse Signal, für das der Zähler erhöht wird.
            rPlant (Plant): Ein Objekt der Klasse Plant, für den der Zähler erhöht wird.

        """
        key = (ec, signal, rPlant)
        if key in self.signalSendingCounters:
            self.signalSendingCounters[ec, signal, rPlant] += 1
        else:
            self.signalSendingCounters[ec, signal, rPlant] = 1

    
    def isSignalAlarmed(self, signal):
        """_summary_
            Überprüft, ob ein Signal bereits einen Alarm ausgelöst hat bzw. ob die Pflanze die das Signal produziert Alarm geschlagen hat. 
            Diese Methode verwendet das 'signalAlarms' Dictionary, um den Status eines Signals zu prüfen.
        Args:
            signal (Signal): Die Klasse Signal, dessen Alarmstatus überprüft werden soll.
        Returns:
            bool: 'True', wenn das Signal einen Alarm ausgelöst hat, andernfalls 'False'.
        """
        return self.signalAlarms.get(signal, False)
    

    def setSignalAlarm(self, signal, status):
        """_summary_
            Setzt den Alarmstatus für ein Signal im 'signalAlarms' Dictionary. 
            Diese Methode wird verwendet, um den Alarmstatus für ein bestimmtes Signal zu ändern.
        Args:
            signal (Signal): Das Signal, für das der Alarmstatus gesetzt werden soll.
            status (bool): Der neue Status des Alarms für das Signal. 'True' für aktivierten Alarm, 'False' für keinen Alarm.
        """
        self.signalAlarms[signal] = status


    def isSignalPresent(self, signal):
        """_summary_
            Überprüft, ob ein Signal im 'isSignalSignaling' Dictionary vorhanden ist. 
            Diese Methode dient dazu, den Status eines Signals zu prüfen, ob es aktuell aktiv ist oder nicht.
        Args:
            signal (Signal): Das Signal, dessen Präsenzstatus überprüft werden soll.

        Returns:
            bool: 'True', wenn das Signal im 'isSignalSignaling' Dictionary vorhanden ist und aktiv ist, andernfalls 'False'.
        """
        return self.isSignalSignaling.get(signal, False)
    

    def setSignalPresence(self, signal, status):
        """_summary_
            Setzt den Präsenzstatus eines Signals in der 'isSignalSignaling' Dictionary. 
            Diese Methode wird verwendet, um den Präsenzstatus eines Signals zu ändern.
        Args:
            signal (Signal): Das Signal, dessen Präsenzstatus gesetzt werden soll.
            status (bool): Der neue Status der Signalpräsenz. 'True' für aktiviert, 'False' für inaktiv.

        """
        self.isSignalSignaling[signal] = status

    
    def enemySignalAlarm(self, signal):
        """_summary_
            Aktiviert einen Alarm für ein Signal im 'signalAlarms' Dictionary. 
            Diese Methode wird verwendet, um anzuzeigen, dass ein Signal alamiert ist bzw. für die Produktion vorbereitet wird.
        Args:
            signal (Signal): Das Signal, das für die Priduktion vorbereitet wird.
        """
        self.setSignalAlarm(signal, True)
    

    def makeSignal(self, signal):
        """_summary_
            Erzeugt ein Signal indem es den Alarmstatus auf 'False' setzt und den Präsenzstatus auf 'True' im 'signalAlarms'- und 'isSignalSignaling' Dictionary. 
            Diese Methode wird verwendet, um ein Signal aktiv zu setzen so dass es von der betroffenen Pflanze ausgestrahlt werden kann.
        Args:
            signal (Signal): Das Signal, das aktiviert werden soll.
        """
        self.setSignalAlarm(signal, False)
        self.setSignalPresence(signal, True)


    def setAfterEffectTime(self, signal, aft):
        """_summary_
            Setzt die Nachwirkungszeit ('aft') für ein Signal im 'afterEffectTimes' Dictionary. 
            Diese Methode wird verwendet, um festzulegen, wie lange ein Signal nach seiner Deaktivierung noch nachwirken soll.
        Args:
            signal (Signal): Das Signal, für das die Nachwirkungszeit gesetzt werden soll.
            aft (int): Die Dauer der Nachwirkungszeit.
        """
        self.afterEffectTimes[self, signal] = aft

    
    def getAfterEffectTime(self, signal):
        """_summary_
            Ruft die Nachwirkungszeit für ein Signal ab. 
            Falls für das Signal keine Nachwirkungszeit definiert ist, wird ein Standardwert von 0 zurückgegeben.
        Args:
            signal (Signal): Das Signal, dessen Nachwirkungszeit abgefragt werden soll.
        Returns:
            int: Die Nachwirkungszeit für das angegebene Signal. Wenn keine Nachwirkungszeit vorhanden ist, wird 0 zurückgegeben.
        """
        key = (self, signal)
        return self.afterEffectTimes.get(key, 0)

    
    def resetToxinProdCounter(self, ec, toxin):
        """_summary_
            Setzt den Produktionszähler für ein Toxin von einem EnemyCluster Objekt auf 0. 
            Diese Methode wird verwendet, um die Produktion eines Giftstoffs für ein EnemyCluster zurückzusetzen.
        Args:
            ec (EnemyCluster): Objek der Klasse EnemyCluster.
            toxin (Toxin): Das Toxin, dessen Produktionszähler zurückgesetzt werden soll.
        """
        self.toxinProdCounters[ec, toxin] = 0


    def incrementToxinProdCounter(self, ec, toxin):
        """_summary_
            Erhöht den Produktionszähler für ein Toxin und einem Objekt von der Klasse EnemyCluster um 1.
            Falls die Kombination aus EnemyCluster und Toxin noch nicht existiert, wird sie hinzugefügt und der Zähler auf 1 initialisiert.
        Args:
            ec (EnemyCluster): Objekt von EnemyCluster, die mit dem Toxin verknüpft ist.
            toxin (Toxin): Das Toxin, dessen Produktionszähler erhöht werden soll.
        """
        key = (ec, toxin)
        if key in self.toxinProdCounters:
            self.toxinProdCounters[ec, toxin] += 1
        else:
            self.toxinProdCounters[ec, toxin] = 1


    def getToxinProdCounter(self, ec, toxin):
        """_summary_
            Gibt den Produktionszähler für ein Toxin und einem EnemyCluste zurück. 
            Falls kein Zähler für die Kombination aus EnemyCluste und Toxin existiert, wird ein Standardwert von 1 zurückgegeben.
        Args:
            ec (EnemyCluster): Objekt von EnemyCluste, die mit dem Toxin verknüpft ist.
            toxin (TOxin): Das Toxin, dessen Produktionszähler abgefragt werden soll.
        Returns:
            int: Der Produktionszähler für die Kombination aus EnemyCluster und Toxin. Wenn kein Eintrag existiert, wird standardmäßig '1' zurückgegeben.
        """
        key = (ec, toxin)
        return self.toxinProdCounters.get(key, 1)
    

    def isToxinAlarmed(self, toxin):
        """_summary_
            Überprüft, ob ein Alarm für ein Toxin aktiviert ist. 
            Diese Methode prüft den Alarmstatus im 'toxinAlarms' Dictionary.
        Args:
            toxin (Toxin): Objekt der Klasse Toxin, dessen Alarmstatus abgefragt werden soll.
        Returns:
            bool: 'True', wenn ein Alarm für das Toxin aktiv ist, andernfalls 'False'.
        """
        return self.toxinAlarms.get(toxin, False)
    

    def setToxinAlarm(self, toxin, status):
        """_summary_
            Setzt den Alarmstatus für ein Toxin im 'toxinAlarms' Dictionary. 
            Diese Methode wird verwendet, um einen Alarm für ein Toxin zu aktivieren oder zu deaktivieren.
        Args:
            toxin (Toxin): Ein Objekt von Toxins, dessen Alarmstatus geändert werden soll.
            status (bool): Der neue Alarmstatus. 'True', um den Alarm zu aktivieren, und 'False', um ihn zu deaktivieren.
        """
        self.toxinAlarms[toxin] = status


    def isToxinPresent(self, toxin):
        """_summary_
            Überprüft, ob ein Toxin aktuell präsent ist. 
            Diese Methode prüft den Präsenzstatus im 'isToxically' Dictionary.
        Args:
            toxin (Toxin): Ein Objekt von Toxins, dessen Präsenzstatus abgefragt werden soll.
        Returns:
            bool: 'True', wenn das Toxin präsent ist, andernfalls 'False'.
        """
        return self.isToxically.get(toxin, False)
    

    def setToxinPresence(self, toxin, status):
        """_summary_
            Legt fest, ob ein Toxin aktuell präsent ist oder nicht. 
            Diese Methode aktualisiert den Präsenzstatus im 'isToxically' Dictionary.
        Args:
            toxin (Toxin): Objekt von Toxins, dessen Präsenzstatus geändert werden soll.
            status (bool): Der neue Präsenzstatus. 'True', wenn das Toxin als präsent markiert werden soll, und 'False', um die Präsenz zu entfernen.
        """
        self.isToxically[toxin] = status

    
    def enemyToxinAlarm(self, toxin):
        """_summary_
            Aktiviert den Alarmstatus für ein Toxin. 
            Diese Methode wird verwendet, um einen Alarm auszulösen, wenn die Produktion von einem Giftstoff ausgelöst wurde.
        Args:
            toxin (Toxin): Ein Objekt von Toxin, was alamiert durch Fressfeinde alamiert wurde.
        """
        self.setToxinAlarm(toxin, True)
    

    def makeToxin(self, toxin):
        """_summary_
            Erzeugt ein Toxin, indem der Alarmstatus des Toxins deaktiviert und dessen Präsenzstatus aktiviert wird.
            Diese Methode wird verwendet, wenn ein neues Toxin erzeugt wird und sein Alarmstatus sowie seine Präsenz aktualisiert werden müssen.
        Args:
            toxin (Toxin): Objekt der Klasse Toxin
        """
        self.setToxinAlarm(toxin, False)
        self.setToxinPresence(toxin, True)


    def getSignalSendCounter(self, ec, signal, rPlant):
        """_summary_
            Gibt den Sendezähler für ein Signal an eine bestimmte Zielpflanze in Kombination mit einem EnemyCluster zurück.
            Falls kein Eintrag für diese Kombination aus EnemyCluster, Signal und Zielpflanze vorhanden ist, wird ein Standardwert von 0 zurückgegeben.
        Args:
            ec (EnemyCluster): EnemyCluster, welches mit dem Signal verknüpft ist.
            signal (Signal): Das Signal, dessen Sendezähler abgefragt werden soll.
            rPlant (Plant): Die Zielpflanze, zu der das Signal gesendet wurde.
        Returns:
            int: Der Sendezähler für die Kombination aus EnemyCluster, Signal und Zielpflanze. 
        """
        key = (ec, signal, rPlant)
        return self.signalSendingCounters.get(key, 0)
    

    def sendSignal(self, rplant, signal):
        """_summary_
            Sendet ein Signal an eine Zielpflanze ('rplant'). Diese Methode wird verwendet, 
            um eine Signal-Präsenz auf der Zielpflanze zu aktivieren, um zu signalisieren, dass ein Signal an sie gesendet wurde.
        Args:
            rplant (Plant): Die Zielpflanze, an die das Signal gesendet wird.
            signal (Signal): Das spezifische Signal, das gesendet wird.
        """
        rplant.setSignalPresence(signal, True)

    
    def airSignalRange(self, signal):
        """_summary_
            Diese Methode prüft, ob der Schlüssel für das aktuelle Signal und die Pflanze bereits im 'radius' Dictionary von 'signal' existiert. 
            Falls der Schlüssel noch nicht vorhanden ist, wird er mit einem Standardwert 0 hinzugefügt. 
            Wenn der Schlüssel bereits existiert, wird keine Änderung vorgenommen. 
            Die Methode gibt den Radiuswert für den entsprechenden Schlüssel zurück.
        Args:
            signal (Signal): Das Signal, das verbreitet werden soll.
        Returns:
            int: Der Ausbreitungsradius des Signals für den aktuellen Schlüssel (Pflanze, Signal).
        """
        key = (self, signal)
        if key in signal.radius:
            pass
        else:
            signal.radius[key] = 0
        return signal.radius[key]
    

    def incrementSignalRadius(self, ec, signal):
        """_summary_
            Erhöht den Zähler für den Ausbreitungsradius eines Signals in kombination mit einem auslösenden EnemyCluster.
            Diese Methode wird verwendet, um den Counter für die Ausbreitung über die Luft zu erhöhen.
        Args:
            ec (EnemyCluster): EnemyCluster, dass das Signal auslöst.
            signal (str): Das Signal, dessen Ausbreitungs-Counter erhöht werden soll.
        """
        key = (ec, signal)
        if key in self.airSpreadCounters:
            self.airSpreadCounters[ec, signal] += 1
        else:
            self.airSpreadCounters[ec, signal] = 1

    
    def getSignalAirSpreadCounter(self, ec, signal):
        """_summary_
            Ruft den Counter für die Ausbreitung eines Signals über die Luft in Verbindung mit einem EnemyCluster ab.
            Wenn keine Counter für die Kombination aus EnemyCluster und Signal vorhanden sind, wird ein Standardwert von 0 zurückgegeben.
        Args:
            ec (EnemyCluster): EnemyCluster, dass mit dem Signal verknüpft ist.
            signal (str): Das Signal, dessen Ausbreitungscounter abgefragt wird.
        Returns:
            int: Der aktuelle Ausbreitungscounter für die Kombination aus EnemyCluster und Signal. 
        """
        key = (ec, signal)
        return self.airSpreadCounters.get(key, 0)
    

    def resetSignalAirSpreadCounter(self, ec, signal):
        """_summary_
            Setzt den Counter für die Ausbreitung eines Signals über die Luft in Verbindung mit einem EnemyCluster auf 0 zurück.
            Diese Methode wird verwendet, um den Counter für eine bestimmte Kombination aus EnemyCluster und Signal auf den Ausgangswert von 0 zurückzusetzen.
        Args:
            ec (EnemyCluster): EnemyCluster, dass mit dem Signal verknüpft ist.
            signal (Signal): Das Signal, dessen Ausbreitungscounter zurückgesetzt werden soll.
        """
        key = (ec, signal)
        if key in self.airSpreadCounters:
            self.airSpreadCounters[key] = 0
