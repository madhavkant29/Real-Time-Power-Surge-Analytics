MAX_HISTORY = 300

class VoltageStorage:
    def __init__(self):
        self.data = []

    def add(self, record: dict):
        self.data.append(record)
        if len(self.data) > MAX_HISTORY:
            self.data.pop(0)

    def get_all(self):
        return self.data

    def get_last_n(self, n: int):
        return self.data[-n:]