def clamp(i, mi, ma):
    """
    clamp a number between a min and max
        :param i: number to clamp
        :param mi: min
        :param ma: max
    """
    return max(min(i, ma), mi)