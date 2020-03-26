def fetch_avg_survey_stats(cursor):
    cursor.execute("""
        SELECT
            DimFacility.name as facility,
            avg(FactSurvey.rating_id) as avgRating
        FROM
            FactSurvey
        LEFT JOIN DimFacility on FactSurvey.facility_id = DimFacility.id
        LEFT JOIN DimRating on FactSurvey.rating_id = DimRating.id
        WHERE
            FactSurvey.rating_id <> 6 AND FactSurvey.rating_id <> 0
        GROUP BY
            FactSurvey.facility_id
    """)
    return cursor.fetchall()

