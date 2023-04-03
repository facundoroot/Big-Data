from typing import Optional

from core.tools.utils.helpers import logger 

from airflow_dbt_python.operators.dbt import DbtRunOperator

import os
from dotenv import load_dotenv

load_dotenv()

LOGGER = logger("taskfactory")

# DBT_PROJECT_AND_PROFILES_DIR: Optional[str] = os.getenv("DBT_TEMPLATES_DIR")

# LOGGER.info(f"DBT_PROJECT_AND_PROFILES_DIR: {DBT_PROJECT_AND_PROFILES_DIR}")

DBT_PROJECT_AND_PROFILES_DIR: str = "/opt/dbt"
def dbt_run_task(model_name: str, task_id: str) -> DbtRunOperator:

    """
    Use DbtRunOperator to run a specific DBT model

    Args:
        * model_name: DBT model name
        * task_id: Airflow task id

    Returns: DbtRunOperator
    """

    dbt_operator: DbtRunOperator = DbtRunOperator(
        task_id=task_id,
        project_dir=DBT_PROJECT_AND_PROFILES_DIR,
        profiles_dir=DBT_PROJECT_AND_PROFILES_DIR,
        models=[model_name],
        full_refresh=False
    )

    return dbt_operator
