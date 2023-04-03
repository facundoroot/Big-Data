import pytest
import yaml

from pathlib import Path
from core.tools.dagfactory.helpers import load_yaml_content
from core.tools.dagfactory.dag_factory import YAML_DEFINED_DAGS_PATH

from typing import Dict, Any

def test_path_object() -> None:

    """
    Test if YAML_DEFINED_DAGS_PATH points to a correct and existing file.

        1. Check if the path is an absolute path.
        2. Check if the file or directory exists.

    If any of these assertions fail, the test will fail.

    Args:
        None

    Returns:
        None
    """


    path: Path = YAML_DEFINED_DAGS_PATH

    assert path.is_absolute()  # Check if the path is absolute
    assert path.exists()  # Check if the path exists


def test_load_yaml_content() -> None:
    """
    Test if `load_yaml_content()` function loads YAML content from a file correctly.

    This function creates a temporary YAML file with some test content, and then calls
    `load_yaml_content()` with the path to the temporary file. It then asserts that
    the function returns a dictionary that matches the expected content of the file.

    If the function raises an error, the test will fail.

    Args:
        * tmp_path: pytest fixture that provides a temporary directory path.

    Returns:
        None
    """

    yaml_files_path: Path =  YAML_DEFINED_DAGS_PATH

    # Create a temporary YAML file with test content
    test_yaml_content: Dict[str, Any] = {'key1': 'value1', 'key2': {'subkey1': 123}}
    test_yaml_path: Path = yaml_files_path / 'test.yaml'

    with open(test_yaml_path, 'w') as f:
        yaml.dump(test_yaml_content, f)

    # Call the function with the path to the temporary file
    result = load_yaml_content(test_yaml_path)

    # Assert that the function returns the expected result
    assert result == test_yaml_content

    # Delete the temporary file
    test_yaml_path.unlink()


