from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

from pathlib import Path

import utils

from typing import List, Dict, Any

import logging
import yaml

logging.basicConfig(
    format='%(name)s-%(asctime)s::%(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('DagFactory')


class DagFactory:

    """
    Creates DAGs to be loaded dynamically
    """

    def __init__(self, yaml_absolute_path: Path):

        self.dag_yaml_path = yaml_absolute_path

    def _load_config_data(self) -> Any:

        """
        Load yaml file content

        Args:
            *   None

        Returns: Content of YAML file
        """

        try:

            with open(
                self.dag_yaml_path,
                encoding="utf-8",
            ) as file:

                data = yaml.safe_load(file)
                LOGGER.info(f"DAG YAML file path: {self.dag_yaml_path}")

        except FileNotFoundError:

            LOGGER.error(f"incorrect file path: {self.dag_yaml_path}")
            raise

        return data


    def _parse_dag_yaml_config(self) -> Dict[str, str]:

        """
        Parses content from YAML to DAG dict

        Args:
            *   None

        Returns: YAML content parsed into a config Dict
        """

        return dict()



    def create_dag(self) -> DAG:

        dag_config = self._load_config_data()
        LOGGER.info(f"dag configuration: {dag_config}")

        with DAG(**dag_config) as dag:

            return dag


def generate_dags() -> Dict[str, DAG]:

    """
    Creates DAGs using dag definitions YAML files.

    Args:
        *   None

    Returns: Dictionary of DAGs created using dag definitions YAML files.
    """

    config_files: List[Path] = list(sorted(utils.DAG_DEFINITIONS_PATH.rglob("*.yml")))
    LOGGER.info(f"{len(config_files)} DAG definitions found: {list(map(str, config_files))}")

    generated_dags: Dict[str, DAG] = {}

    for yaml_file in config_files:

        yaml_absolute_path: Path = yaml_file.resolve()
        dag_factory: DagFactory = DagFactory(
            yaml_absolute_path=yaml_absolute_path
        )
        dag = dag_factory.create_dag()
        generated_dags[dag.dag_id] = dag

    return generated_dags
