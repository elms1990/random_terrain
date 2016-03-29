import numpy as np

from utils.filters import medianFilter
from utils.array import normalize
from terrain.terrain_converter import TerrainConverter

class ValueNoise:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def generate(self, levels=10, smoothFactor=1, gaussianSmooth=1.5):
        return self.__generateNoise__(levels, smoothFactor, gaussianSmooth)

    def __interpolate__(self, noise, x, y):
        fractX = x - int(x)
        fractY = y - int(y)

        x1 = (int(x) + self.w) % self.w
        y1 = (int(y) + self.h) % self.h
        x2 = (x1 + self.w - 1) % self.w
        y2 = (y1 + self.h - 1) % self.h

        value = 0.0
        value += fractX * fractY * noise[y1][x1]
        value += (1 - fractX) * fractY * noise[y1][x2]
        value += fractX * (1 - fractY) * noise[y2][x1]
        value += (1 - fractX) * (1 - fractY)  * noise[y2][x2]

        return noise[y, x]

    def __turbulence__(self, levels, lPO2, noise, x, y):
        l = lPO2
        v = 0
        ll = 1
        while l >= 1:
            v += self.__interpolate__(noise, x / l, y / l) * ll
            l /= 2
            ll += 1

        return v / (levels + 1)

    def __generateNoise__(self, levels, smoothFactor, gaussianSmooth):
        noise = np.random.rand(self.w, self.h)
        terrain = np.zeros((self.w, self.h), np.float)

        lPO2 = 2 ** levels
        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                terrain[y, x] = self.__turbulence__(levels, lPO2, noise, x * smoothFactor, y * smoothFactor)

        terrain = medianFilter(terrain)
        normalize(terrain)
        return terrain
