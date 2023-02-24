import os

from src.airflow.dags.source.dynamic_dags import utils


def test_yaml_defined_dags_folder() -> None:

    """
    If the folder is empty then finish, else check if files are YAML

    Args:
        *   None

    Returns: None
    """

    DAG_DEFINITIONS_PATH: str = str(utils.DAG_DEFINITIONS_PATH)

    if not os.listdir(DAG_DEFINITIONS_PATH):

        return
    else:

        files = os.listdir(DAG_DEFINITIONS_PATH)

        for file in files:
            assert file.endswith('.yaml'), f"{file} does not have a .yaml extension"
