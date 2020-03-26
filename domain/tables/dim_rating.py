from enum import Enum

TABLE_NAME = 'DimRating'


class Rating(Enum):
    BLANK = 0
    UNACCEPTABLE = 1
    BELOW_AVERAGE = 2
    AVERAGE = 3
    GOOD = 4
    OUTSTANDING = 5
    NEVER_USED_OR_VISITED = 6
