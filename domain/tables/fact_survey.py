from dataclasses import dataclass

TABLE_NAME = 'FactSurvey'

@dataclass
class Survey:
    """Maps to a row in the rating table"""
    resp_num: int
    date: int
    facility_id: int
    rating_id: int
