import numpy as np
import random
from utils.filters import medianFilter

TERRAIN_UNASSIGNED = -1
TERRAIN_LAND = 0
TERRAIN_WATER = 1

class Sparks:
    neighborMask = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def generateTerrain(self, initialScatter='auto', landProb=0.8, smoothingIterations=8):
        if initialScatter == 'auto':
            initialScatter = (self.w * self.h) * 0.10
        terrain = np.zeros((self.w, self.h), dtype=np.int8)
        terrain.fill(TERRAIN_UNASSIGNED)

        sparkList = []
        while len(sparkList) < initialScatter:
            point = (random.randint(0, self.w - 1), random.randint(0, self.h - 1))
            terrain[point[1], point[0]] = TERRAIN_LAND
            sparkList.append(point)

        while len(sparkList) > 0:
            pos = random.randint(0, len(sparkList) - 1)
            x, y = sparkList[pos]
            del sparkList[pos]

            if terrain[y, x] == TERRAIN_LAND:
                for m in Sparks.neighborMask:
                    nX = x + m[0]
                    nY = y + m[1]

                    if nX < 0 or nX >= self.w or nY < 0 or nY >= self.h:
                        continue

                    if terrain[nY, nX] == TERRAIN_UNASSIGNED:
                        prob = random.uniform(0, 1)

                        if prob <= landProb:
                            terrain[nY, nX] = TERRAIN_LAND
                        else:
                            terrain[nY, nX] = TERRAIN_WATER

                        sparkList.append((nX, nY))
            else:
                for m in Sparks.neighborMask:
                    nX = x + m[0]
                    nY = y + m[1]

                    if nX < 0 or nX >= self.w or nY < 0 or nY >= self.h:
                        continue

                    if terrain[nY, nX] == TERRAIN_UNASSIGNED:
                        terrain[nY, nX] = TERRAIN_WATER

                        sparkList.append((nX, nY))

        for _ in xrange(smoothingIterations):
            terrain = medianFilter(terrain)

        return terrain
