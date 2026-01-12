import yaml
from pathlib import Path
from typing import Dict, Any
import logging


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file and return its contents as a dictionary.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Parsed YAML configuration.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the YAML file is empty or invalid.
    """

    config_path = Path(config_path)

    try:
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_path}")

        with config_path.open('r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            '''Utf-8 encoding is used to get all the special characters too in the yaml file correctly'''
        logging.info(f"Configuration file [{config_path}] loaded successfully")

    except:
        if config is None:
            raise ValueError(f"Config file at {config_path} is empty or invalid")
        '''raises error if config is empty or invalid'''
        logging.error(f"Error loading configuration file at {config_path}")
        raise

    logging.info("Config loaded successfully")
    logging.info("Config keys: %s", list(config.keys()))
    return config