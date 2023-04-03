import yaml

from project.tools.utils.helpers import logger

from pathlib import Path

from typing import List, Optional, Dict, Any

LOGGER = logger('dagfactory-helpers')

def get_yaml_files_path(yaml_defined_dags_path: Path) -> Optional[List[Path]]:

    """
    Gets paths of .yaml files inside yaml_defined_dags folder

    Args:
        * yaml_defined_dags_path(Path): path to yaml_defined_dags folder

    Returns: List of paths of YAML files
    """
    
    yaml_files_path: List[Path] = list(
            sorted(yaml_defined_dags_path.rglob("*.yaml"))
        )
        
    if not yaml_files_path:

        LOGGER.warning("There are no YAML defined DAGs")
    else:

        LOGGER.info(
            f"{len(yaml_files_path)} YAML defined dags found: {yaml_files_path}"
        )
    
    return yaml_files_path


def load_yaml_content(dag_yaml_path: Path) -> Dict[str, Any]:
    
    """
    Load content of YAML file

    Args:
        * dag_yaml_path: Path of YAML with dag configurations

    Returns: Dictionary of YAML content
    """

    try:

        with open(dag_yaml_path, encoding="utf-8") as file:

            yaml_content: Dict[str, Any] = yaml.safe_load(file)
    except FileNotFoundError:

        LOGGER.error(f"No such file or can't be opened: {dag_yaml_path}")
        raise

    return yaml_content


