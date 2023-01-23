class Battery:
    def __init__(self):
        self.current = 1000
        self.max = 1000
        self.bar_length = 400
        self.ratio = self.max / self.bar_length

    def damage(self, amount):
        self.current = max(0, self.current - amount)

    def charge(self, amount):
        self.current = min(self.max, self.current + amount)

    def get_max(self):
        return self.max

    def get_current(self):
        return self.current

    def get_ratio(self):
        return self.ratio

    def get_bar_len(self):
        return self.bar_length

    def can_move(self):
        return self.current > 0
