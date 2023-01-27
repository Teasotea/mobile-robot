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

    def getMax(self):
        return self.max

    def getCurrent(self):
        return self.current

    def getRatio(self):
        return self.ratio

    def getBarLen(self):
        return self.bar_length

    def canMove(self):
        return self.current > 0
