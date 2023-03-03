import yaml
import logging
import os

from pathlib import Path
from typing import Dict, List

logging.basicConfig(
    format='%(name)s - %(asctime)s:: %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('DagFactory-utils')

DAG_DEFINITIONS_PATH: Path = Path(__file__).parent.parent.parent / 'yaml_defined_dags'


def list_yaml_files_names() -> List[str]:

    """
    List YAML files from dag definitions folder

    Returns: List of file names from dag definitions folder
    """

    dag_definitions_path: str = str(DAG_DEFINITIONS_PATH)

    file_names = []

    if not os.listdir(dag_definitions_path):
        LOGGER.warning(f"empty directory: {dag_definitions_path}")
    else:

        file_names: List[str] = [file for file in os.listdir(DAG_DEFINITIONS_PATH)]

    LOGGER.info(f"yaml files names: {file_names}")
    return file_names


def yaml_parser(dag_name: str) -> Dict[str, str]:

    """
    Parses YAML files

    Args:
        *   dag_name(str): name of yaml dag to parse into a dict

    Returns: Parsed content from YAML to dict.
    """

    dag_definition_path: Path = DAG_DEFINITIONS_PATH / dag_name

    try:

        with open(dag_definition_path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            LOGGER.info(f"YAML file definition on path: {dag_definition_path}")

    except FileNotFoundError:

        LOGGER.error(f"incorrect file path: {dag_definition_path}")
        raise

    return data
