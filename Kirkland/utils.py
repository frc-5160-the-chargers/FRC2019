# utils.py
# standard utilities and functions that aren't in the python stl for some reason

# clamp a number between a min and a max
def clamp(i, minNum, maxNum):
    return max(min(i, maxNum), minNum)