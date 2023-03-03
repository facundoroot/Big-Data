from pathlib import Path

import logging

logging.basicConfig(
    format='%(name)s - %(asctime)s:: %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('DAG-helpers')


QUERY_TEMPLATES_LOCATION = Path(__file__).parent.parent.parent / 'queries'


def get_query_path(query_template_path: str) -> str:

    """
    Returns full path for specific SQL file

    Args:
        *   query_template_path (str): path to SQL file starting from /queries as root for example: datawarehouse/example.sql

    Returns: full path for specific SQL file
    """

    return (
        (QUERY_TEMPLATES_LOCATION / query_template_path)
        .with_suffix('.sql')
        .absolute()
        .as_posix()
    )


def load_query_template(query_template_path: str) -> str:

    """
    Get query inside SQL file:

    Args:
        *   query_template_path: path to query with /queries as root
            for example: airflow/datawarehouse/example.sql

    Returns: Query string of SQL file
    """

    sql_file_path: str = get_query_path(
        query_template_path=query_template_path
    )

    try:

        with open(sql_file_path) as file:
            query: str = file.read()

    except FileNotFoundError:

        LOGGER.info(
            f"incorrect path provided: {sql_file_path}"
        )
        raise

    return query
