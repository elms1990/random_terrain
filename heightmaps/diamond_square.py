import numpy as np
import random

from utils.array import normalize
from utils.filters import medianFilter

class DiamondSquare:
    def __init__(self, dim):
        self.dim = dim

    def generate(self, sampleSize=16, roughness=1.6):
        return self.__generateNoise__(sampleSize, roughness)

    def __sampleWithNoise__(self, sampleSize, scale):
        return (random.uniform(0, 1) * 2 - 1) * sampleSize * scale

    def __generateNoise__(self, sampleSize, roughness):
        noise = np.zeros((self.dim, self.dim), np.float)

        scale = 1.0 / self.dim
        noise[0, 0] = self.__sampleWithNoise__(sampleSize, scale)
        noise[0, self.dim - 1] = self.__sampleWithNoise__(sampleSize, scale)
        noise[self.dim - 1, 0] = self.__sampleWithNoise__(sampleSize, scale)
        noise[self.dim - 1, self.dim - 1] = self.__sampleWithNoise__(sampleSize, scale)
    
        while sampleSize > 1:
            self.__diamondSquare__(noise, sampleSize, scale)
            scale *= roughness
            sampleSize /= 2

        nois = medianFilter(noise)
        normalize(noise)
        
        return noise

    def __diamondSquare__(self, noise, sampleSize, scale):
        step = sampleSize / 2
        for y in xrange(0, self.dim - 1, step):
            for x in xrange(0, self.dim - 1, step):
                self.__diamondStep__(noise, sampleSize, scale, x, y, step)
        for y in xrange(0, self.dim - 1, step):
            for x in xrange(0, self.dim - 1, step):
                self.__squareStep__(noise, sampleSize, scale, x, y, step)

    def __diamondStep__(self, noise, sampleSize, scale, x, y, length):
        xFinal, yFinal = x + length, y + length
        average = (noise[y, x] + noise[yFinal, x] + noise[y, xFinal] + noise[yFinal, xFinal]) / 4

        xMiddle, yMiddle = x + length / 2, y + length / 2
        noise[yMiddle, xMiddle] = average + self.__sampleWithNoise__(sampleSize, scale)

    def __squareStep__(self, noise, sampleSize, scale, x, y, length):
        xFinal, yFinal = x + length, y + length
        xMiddle, yMiddle = x + length / 2, y + length / 2

        noise[yMiddle, x] = (noise[y][x] + noise[yFinal][x] + noise[yMiddle, xMiddle]) / 3 + self.__sampleWithNoise__(sampleSize, scale)
        noise[y, xMiddle] = (noise[y][x] + noise[y][xFinal] + noise[yMiddle, xMiddle]) / 3 + self.__sampleWithNoise__(sampleSize, scale)
        noise[yFinal][xMiddle] = (noise[yFinal][xFinal] + noise[yFinal][x] + noise[yMiddle, xMiddle]) / 3 + self.__sampleWithNoise__(sampleSize, scale)
        noise[yMiddle][xFinal] = (noise[yFinal][xFinal] + noise[y][xFinal] + noise[yMiddle, xMiddle]) / 3 + self.__sampleWithNoise__(sampleSize, scale)
