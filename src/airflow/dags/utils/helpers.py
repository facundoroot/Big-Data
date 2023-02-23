from pathlib import Path


QUERY_TEMPLATES_LOCATION = Path(__file__).parent.parent / 'queries'

print("path: ", str(QUERY_TEMPLATES_LOCATION))


def get_query_path(query_template_path: str) -> str:
    return (
        (QUERY_TEMPLATES_LOCATION / query_template_path)
        .with_suffix('.sql')
        .absolute()
        .as_posix()
    )


def load_query_template(query_template_path: str) -> str:

    """
    Load query template:
        *   query_template_path: path to query with /queries as root
            for example: airflow/analytics/example.sql

        returns: query string
    """

    with open(
        get_query_path(
            query_template_path=query_template_path
        )
    ) as file:

        query: str = file.read()

    return query
