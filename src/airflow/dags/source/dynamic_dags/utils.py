import yaml
import logging

from pathlib import Path
from typing import Dict

logging.basicConfig(
    format='%(name)s - %(asctime)s:: %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('DagFactory-utils')

DAG_DEFINITIONS_PATH: Path = Path(__file__).parent.parent.parent / 'yaml_defined_dags'


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
