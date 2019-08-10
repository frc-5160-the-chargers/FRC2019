# utils.py
# standard utilities and functions that aren't in the python stl for some reason


def clamp(i, minNum, maxNum):
    # clamp a number between a min and a max
    return max(min(i, maxNum), minNum)
