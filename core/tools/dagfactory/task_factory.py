from typing import Optional

from core.tools.utils.helpers import logger

from airflow_dbt_python.operators.dbt import DbtRunOperator, DbtTestOperator
from airflow.utils.task_group import TaskGroup

from dotenv import load_dotenv

load_dotenv()

LOGGER = logger("taskfactory")

DBT_PROJECT_AND_PROFILES_DIR: str = "/opt/dbt"

def dbt_run_task(model_name: str, task_id: str) -> DbtRunOperator:

    """
    Use DbtRunOperator to run a specific DBT model

    Args:
        * model_name: DBT model name
        * task_id: Airflow task id

    Returns: DbtRunOperator
    """

    with TaskGroup(group_id=model_name) as model_tg:

        dbt_run_model: DbtRunOperator = DbtRunOperator(
            task_id=f"run_{model_name}_model",
            project_dir=DBT_PROJECT_AND_PROFILES_DIR,
            profiles_dir=DBT_PROJECT_AND_PROFILES_DIR,
            models=[model_name],
            full_refresh=False
        )

        dbt_test_model: DbtTestOperator = DbtTestOperator(
            task_id=f"test_{model_name}_model",
            project_dir=DBT_PROJECT_AND_PROFILES_DIR,
            profiles_dir=DBT_PROJECT_AND_PROFILES_DIR,
            models=[model_name]
        )

        dbt_run_model >> dbt_test_model

    return model_tg
