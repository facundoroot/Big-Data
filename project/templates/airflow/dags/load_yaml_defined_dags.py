from typing import Dict
from airflow import DAG

from project.tools.dagfactory.dag_factory import load_yaml_defined_dags

dags: Dict[str, DAG] = load_yaml_defined_dags()

print(f"created_dags: {load_yaml_defined_dags}")
globals().update(dags)
