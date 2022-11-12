from numpy import sqrt, mean, std

def euclidean(a, b):
    return sqrt(sum((val1-val2)**2 for val1, val2 in zip(a,b)))

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def final_metrics(dists):
    return mean(dists), std(dists)