class Trash:
    def __init__(self):
        self.max_size = 10
        self.current_size = 0

    def add(self):
        self.current_size += 1 if self.is_not_full() else 0

    def is_not_full(self):
        return self.current_size < self.max_size

    def clean(self):
        self.current_size = 0

    def is_empty(self):
        return self.current_size == 0

    def get_current_size(self):
        return self.current_size

    def get_max_size(self):
        return self.max_size
