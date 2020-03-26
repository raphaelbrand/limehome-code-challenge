from enum import Enum

TABLE_NAME = 'DimFacility'


class Facility(Enum):
    ARTWORK_AND_EXHIBITIONS = 0
    RESTAURANTS = 1
    RETAIL_SHOPS_AND_CONCESSIONS = 2


class FacilityKeys(Enum):
    q8a = 0
    q8b = 1
    q8c = 2
