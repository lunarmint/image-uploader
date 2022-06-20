import logging
import os

from pyaml_env import parse_config

log = logging.getLogger(__name__)

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
if not os.path.isfile(config_path):
    log.error("Failed to load config.yml.")
    raise SystemExit

config = parse_config(config_path)
