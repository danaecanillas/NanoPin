from numpy import sqrt

def euclidean(a, b):
    return sqrt(sum((val1-val2)**2 for val1, val2 in zip(a,b)))

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))