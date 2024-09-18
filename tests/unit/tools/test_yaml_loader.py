import pytest
import yaml
from src.tools.yaml_loader import load_yaml_file


def test_load_yaml_file(tmp_path):
    # Create a temporary YAML file
    yaml_content = """
    key1: value1
    key2:
      subkey1: subvalue1
      subkey2: subvalue2
    """
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(yaml_content)

    # Expected result
    expected_data = {
        "key1": "value1",
        "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"},
    }

    # Test the function
    result = load_yaml_file(yaml_file)
    assert result == expected_data

    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        load_yaml_file("non_existent_file.yaml")
