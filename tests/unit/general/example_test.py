from src.airflow.dags.source.dynamic_dags.example import sm


def test_sm() -> None:

    """Test sm"""

    assert sm(2, 2) == 4
