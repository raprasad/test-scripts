"""
For printing to the screen
"""
def msg(m): print(m)
def dashes(cnt=40): msg('-' * cnt)
def msgt(m): dashes(); msg(m); dashes()
