import numpy as np

NEIGHBORS_MASK = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

def medianFilter(arr):
    h, w = arr.shape
    filtered = np.zeros(arr.shape, dtype=arr.dtype)

    for y in xrange(h):
        for x in xrange(w):
            s = []
            for n in NEIGHBORS_MASK:
                nX, nY = n
                s.append(arr[(y + nY) % h, (x + nX) % w])
            s.sort()

            filtered[y, x] = s[len(s) / 2]
    return filtered

def meanFilter(arr, windowSize=3):
    h, w = arr.shape
    filtered = np.zeros(arr.shape, dtype=np.float)
    
    halfSize = windowSize / 2
    sizeSqr = windowSize * windowSize
    for y in xrange(h):
        for x in xrange(w):

            s = 0
            for wY in xrange(-halfSize, halfSize + 1):
                for wX in xrange(-halfSize, halfSize + 1):
                    s += arr[(y + wY) % h, (x + wX) % w]
            filtered[y, x] = s / sizeSqr
    return filtered
