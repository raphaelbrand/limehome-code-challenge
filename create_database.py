import json
import urllib
from dataclasses import fields

import config
from domain.tables import fact_survey, dim_facility, dim_rating, dim_date
from domain.tables.dim_facility import Facility, FacilityKeys
from domain.tables.dim_rating import Rating
from domain.tables.fact_survey import Survey
import urllib.request

_SQL_TYPE_MAPPING = {
    int: 'NUMERIC'
}


def _get_fields_and_types(data_class):
    return {field.name: field.type for field in fields(data_class)}


def _generate_dim_table_sql(table_name):
    """

    :param table_name: the table name for the new table
    :return: sql statement to create table
    """

    return f"""
    CREATE TABLE {table_name} (
        id NUMERIC PRIMARY KEY,
        name TEXT
    );
    """


def _generate_fact_table_sql(table_name, data_class):
    """

    :param table_name:
    :return:

    """
    fields = _get_fields_and_types(data_class)
    sql_fields = ',\n'.join(
        f"{column_name} {_SQL_TYPE_MAPPING[column_type]}" for column_name, column_type in fields.items()
    )
    return f"""
    CREATE TABLE {table_name} (
        {sql_fields}
    );
    """


def _enum_to_dim_table(table_name, enum):
    values = ',\n'.join(f'({item.value}, "{item.name}")' for item in enum)
    return f"""
        INSERT INTO {table_name}(id, name) 
        VALUES
        {values}
        ;
    """


# NOTE: This is pretty ugly, but should do for this task. (sorry for this...)
def _create_dates_table():
    values = f"""
    INSERT INTO {dim_date.TABLE_NAME}(id, name)
    VALUES
        (1, "2011-05-10"),
        (2, "2011-05-11"),
        (3, "2011-05-12"),
        (4, "2011-05-13"),
        (5, "2011-05-14"),
        (6, "2011-05-15"),
        (7, "2011-05-16"),
        (8, "2011-05-17"),
        (9, "2011-05-18"),
        (10, "2011-05-19"),
        (11, "2011-05-20"),
        (12, "2011-05-21"),
        (13, "2011-05-22"),
        (14, "2011-05-23"),
        (15, "2011-05-24"),
        (16, "2011-05-25"),
        (17, "2011-05-26"),
        (18, "2011-05-27"),
        (19, "Other"),
        (20, "Unknown")
    """
    return (
        _generate_dim_table_sql(dim_date.TABLE_NAME),
        values
    )


def _create_dim_table(table_name, enum):
    return (
        _generate_dim_table_sql(table_name),
        _enum_to_dim_table(table_name, enum)
    )


def _load_surveys(surveys):
    values = ',\n'.join(
        f'({item.resp_num}, "{item.date}", "{item.facility_id}", "{item.rating_id}")' for item in surveys
    )
    return f"""
    INSERT INTO {fact_survey.TABLE_NAME}(resp_num, date, facility_id, rating_id)
    VALUES
    {values}
    ;
    """


def _execute(cursor, statements):
    for statement in statements:
        cursor.execute(statement)


def _run_migrations(conn):
    cursor = conn.cursor()
    _execute(cursor, _create_dim_table(dim_facility.TABLE_NAME, Facility))
    _execute(cursor, _create_dim_table(dim_rating.TABLE_NAME, Rating))
    _execute(cursor, _create_dates_table())
    _execute(cursor, [_generate_fact_table_sql(fact_survey.TABLE_NAME, Survey)])
    conn.commit()


def _load_data(conn, raw_data):
    cursor = conn.cursor()
    _execute(cursor, [_load_surveys(_preprocess(raw_data))])


def _download_file(url):
    """
    Note: This function is not memory safe. Usually it is better to download the
    file to disk and then stream into memory in case the web server doesn't support a streaming response.
    For simplicity we will do everything in memory here. Also usually it would be easier to use the requests
    library.
    :param url:  the url from where to download the file

    :return the content behind the url
    """
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')


def _preprocess(raw_data):
    """
    :param raw_data: the sfo airport data as received from the api
    :return: rows of dictionaries
    """
    for survey in raw_data:
        for facility in FacilityKeys:
            yield Survey(
                resp_num=int(survey['respnum']),
                date=int(survey['intdate']),
                facility_id=facility.value,
                rating_id=int(survey[facility.name])
            )


def setup_database(db_name, raw_data):
    import sqlite3
    conn = sqlite3.connect(db_name)
    _run_migrations(conn)
    _load_data(conn, raw_data)
    conn.commit()
    return conn


if __name__ == '__main__':
    setup_database(config.DATABASE_NAME, json.loads(_download_file(config.REMOTE_FILE)))
