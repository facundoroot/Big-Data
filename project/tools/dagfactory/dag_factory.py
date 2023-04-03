from airflow.models.dag import DAG

from project.tools.utils.helpers import logger 
from project.tools.dagfactory.helpers import get_yaml_files_path, load_yaml_content
from project.tools.dagfactory.task_factory import dbt_run_task

from pathlib import Path
from datetime import datetime, timedelta
from copy import deepcopy

from typing import Dict, List, Optional, Union, Any

# path to yaml_defined_dag folders
PATH_TO_YAMLS_FROM_PROJECT_DIR: str = 'templates/airflow/dags/yaml_defined_dags'
YAML_DEFINED_DAGS_PATH: Path = Path(__file__).parent.parent.parent / PATH_TO_YAMLS_FROM_PROJECT_DIR

# default arguments for DAG creation
DEFAULT_START_DATE = "2023-09-01"
DEFAULT_ARGS = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": True,
}
DAG_ARGS = {"max_active_runs": 1}

# logger
LOGGER = logger('dagfactory')

class DagFactory:

    def __init__(self, yaml_file_path: Path) -> None:

        self.yaml_file_path = yaml_file_path

    def _parse_dag_configuration(self) -> Dict[str, Union[list, str]]:

        """
        Parse DAG configuration section of of YAML file so it can be
        used later DAG creation

        Args:
            * None
        
        Returns: Dict[str, Any]
        """
        
        yaml_content = load_yaml_content(
            dag_yaml_path=self.yaml_file_path
        )
        
        try:
            dag_configuration: Dict[str, Any] = yaml_content["dag_config"]
        except Exception as e:

            LOGGER.error(f"failed to load dag_config from yaml_content: {e}")
            raise
        # start date
        start_date = dag_configuration.get("start_date", DEFAULT_START_DATE)
        dag_configuration["start_date"] = datetime.strptime(start_date, "%Y-%m-%d") 
        
        #default args
        default_args = dag_configuration.get("default_args", {})
        default_args.update(DEFAULT_ARGS)
        dag_configuration['default_args'] = deepcopy(default_args)

        # tags
        tag_list = dag_configuration.get("tags", "")
        if isinstance(tag_list, str):
            tag_list = tag_list.split(",")
        dag_configuration["tags"] = (
            list(set(tag for tag in map(lambda s: str(s).strip(), tag_list) if len(tag) > 0))
            or None
        )

        dag_configuration.update(DAG_ARGS)

        LOGGER.info(f"dag configuration: {dag_configuration}")

        return dag_configuration


    def _parse_dag_tasks_plans(self) -> Dict[str, Any]:
        
        """
        Parse tasks configuration of YAML file so it can be
        used later for DAG creation

        Args:
            * None
        
        Returns: Dict[str, Any]
        """

        yaml_content = load_yaml_content(
            dag_yaml_path=self.yaml_file_path
        )

        tasks_plans: Dict[str, Any] = yaml_content["dag_tasks_plans"]
        
        return tasks_plans

    def create_dag(self) -> DAG:

        """
        Create DAG object using yaml configuration

        Args:
            * None

        Returns: DAG
        """
        
        LOGGER.info("creating DAG")

        dag_args: Dict[str, Any] = self._parse_dag_configuration()
        LOGGER.info(f"dag_args: {dag_args}")

        dag_tasks_plans: Dict[str, Any] = self._parse_dag_tasks_plans()
        LOGGER.info(f"dag_tasks_plans: {dag_tasks_plans}")
        
        model_name: str = dag_tasks_plans["models_name"][0]
        task_id: str = "dbt_run_" + model_name

        with DAG(**dag_args) as dag:

            dbt_task = dbt_run_task(
                model_name=model_name,
                task_id=task_id
            )

            dbt_task


        return dag


def load_yaml_defined_dags() -> Dict[str, DAG]:
    
    """
    Load DAGs created using YAML files for config

    Args:
        * None

    Returns: Dict with "dag_id": DAG
    """

    dags: Dict[str, DAG] = {}

    yaml_defined_dags_paths: Optional[List[Path]] = get_yaml_files_path(
        yaml_defined_dags_path=YAML_DEFINED_DAGS_PATH
    )

    if not yaml_defined_dags_paths:

        LOGGER.info("No YAML defined dags")

        return dags

    for yaml_file_path in yaml_defined_dags_paths:
        
        dag_factory: DagFactory = DagFactory(yaml_file_path=yaml_file_path)
        dag: DAG = dag_factory.create_dag()
        dags[dag.dag_id] = dag

    
    return dags

