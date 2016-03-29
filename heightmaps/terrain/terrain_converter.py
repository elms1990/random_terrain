class TerrainConverter:
    def __init__(self):
        self.intervals = []

    def add(self, lower, upper, t, value):
        self.intervals.append((lower, upper, t, value))

    def get(self, value):
        for x in self.intervals:
            if value >= x[0] and value <= x[1]:
                return (x[2], x[3])
