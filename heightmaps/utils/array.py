import numpy as np

def normalize(arr):
    minH = arr.min()
    maxH = arr.max()

    h, w = arr.shape
    for y in xrange(h):
        for x in xrange(w):
            arr[y, x] = (arr[y, x] - minH) / (maxH - minH)

    return arr
