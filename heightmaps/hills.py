import math
import numpy as np
import random

class Hills:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __flattenTerrain__(self, terrain):
        return np.sqrt(terrain)

    def __normalizeTerrain__(self, terrain):
        minH = terrain.min()
        maxH = terrain.max()

        h, w = terrain.shape
        for y in xrange(h):
            for x in xrange(w):
                terrain[y,x] = (terrain[y,x] - minH) / (maxH - minH)

    def __addHill__(self, terrain, x1, y1, r):
        rr = r * r

        h, w = terrain.shape
        for y in xrange(-r, r + 1):
            for x in xrange(-r, r + 1):
                z = rr - (x ** 2 + y ** 2)
                tX, tY = x1 + x, y1 + y
                if z >= 0 and tY >= 0 and tY < h and tX >= 0 and tX < w:
                    terrain[y1 + y, x1 + x] += z

    def generateTerrain(self, minRadius=5, maxRadius=19, iterations=200):
        if iterations == 'auto':
            iterations = int(math.ceil((self.w * self.h) * 0.07))
        terrain = np.zeros((self.w, self.h), dtype=np.float)

        for _ in xrange(iterations):
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            r = int(math.ceil(random.uniform(minRadius, maxRadius)))
            
            self.__addHill__(terrain, x, y, r)
           
        self.__normalizeTerrain__(terrain)
        return self.__flattenTerrain__(terrain)
