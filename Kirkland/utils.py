import math

def clamp(i, mi, ma):
    """
    clamp a number between a min and max
        :param i: number to clamp
        :param mi: min
        :param ma: max
    """
    return max(min(i, ma), mi)

def root(i, n):
    """
    take nth root of i
    """
    x = abs(i)
    a = x ** (1./n)
    return math.copysign(a, i)