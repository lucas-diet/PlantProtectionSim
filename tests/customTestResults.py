
import unittest

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