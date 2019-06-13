class Compatibility:

    def __init__(self, clauses):
        self.clauses = clauses

    def check(self):
        return all(self.evaluate())

    def evaluate(self):
        return [c() for c in self.clauses]
