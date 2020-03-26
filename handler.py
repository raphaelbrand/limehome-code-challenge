import json
import sqlite3

import config
from repository.survey.survey import fetch_avg_survey_stats

# keep it warm between runs
connection = sqlite3.connect(config.DATABASE_NAME)
connection.row_factory = sqlite3.Row


def survey_avg(event, context):
    cursor = connection.cursor()

    body = {
        "metrics": [dict(row) for row in fetch_avg_survey_stats(cursor)]
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def ui(event, context):
    with open('ui/ratings.html', 'r') as f:
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": f.read()
        }
