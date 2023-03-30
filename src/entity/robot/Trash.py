class Trash:
    def __init__(self):
        self.max_size = 10
        self.current_size = 0

    def add(self):
        self.current_size += 1 if self.isNotFull() else 0

    def isNotFull(self):
        return self.current_size < self.max_size

    def isFull(self):
        return self.current_size >= self.max_size

    def clean(self):
        self.current_size = 0

    def isEmpty(self):
        return self.current_size == 0

    def getCurrentSize(self):
        return self.current_size

    def getMaxSize(self):
        return self.max_size
