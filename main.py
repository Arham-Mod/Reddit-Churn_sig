import logging
from src.logging import logger  
from src.config.load_config import load_yaml_config


def main():
    try:
        config = load_yaml_config("src/config/reddit.yaml")
        logging.info("Config loaded successfully")
        logging.info("Config keys: %s", list(config.keys()))
    except Exception:
        logging.exception("Failed to load configuration")
        raise


if __name__ == "__main__":
    logger.logging.info("Starting the Reddit Churn Prediction Application")
    main()
