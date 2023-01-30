
from Patterns import PatternsBase

class Square(PatternsBase):

    # The Pattern
    PATTERN = [[50,50], [-50,50], [-50,-50], [-50, 50]]

    def __init__(self):
        super(self, Square.PATTERN)