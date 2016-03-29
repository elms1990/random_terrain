import math
import numpy as np
import random
from utils.filters import meanFilter
from utils.array import normalize

class ParticleDeposition:
    neighborMask = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def generateTerrain(self, dropPoints, maxStabilityRadius, minParticles, maxParticles,
            iterations):
        terrain = np.zeros((self.w, self.h), dtype=np.float)

        for _ in xrange(iterations):
            for d in xrange(dropPoints):
                nParticles = random.randint(minParticles, maxParticles)
                dropX = random.randint(maxStabilityRadius, self.w - maxStabilityRadius - 1)
                dropY = random.randint(maxStabilityRadius, self.h - maxStabilityRadius - 1)
                for x in xrange(nParticles):
                    pX, pY = dropX, dropY

                    stabilityRange = random.randint(1, maxStabilityRadius)
                    for s in xrange(stabilityRange):
                        random.shuffle(ParticleDeposition.neighborMask)

                        stable = True
                        for n in ParticleDeposition.neighborMask:
                            if terrain[pY, pX] > terrain[pY + n[1], pX + n[0]]:
                                stable = False
                                pX = pX + n[0]
                                pY = pY + n[1]
                                break

                        if stable:
                            break
                    terrain[pY, pX] += 1
            dropPoints /= 2
            minParticles = int(math.ceil(minParticles * 0.9))
            maxParticles = int(math.ceil(maxParticles * 0.9))

        return normalize(terrain)
