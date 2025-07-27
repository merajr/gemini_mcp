class ChatMemory:
    def __init__(self):
        self.history = []

    def add(self, role, message):
        self.history.append((role, message))

    def get_recent(self, n=6):
        return self.history[-n:]
