import logging
import os

from pyaml_env import parse_config

log = logging.getLogger(__name__)

if not os.path.isfile("config.yml"):
    log.error("Unable to load config.yml, exiting...")
    raise SystemExit

config = parse_config("config.yml")
