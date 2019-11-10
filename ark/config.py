"""
Configuration for Ark.
"""

import os
import json
from typing import Dict, Optional
from xdg import BaseDirectory


CONFIG_DIR = "ark"
CONFIG_FILE = "ark.json"


def get_config() -> Optional[Dict[str, str]]:
    """Does [...]

    :returns: [...]
    :raises KeyError: When [...]
    """
    # Get base directory, create if missing
    base_dir = BaseDirectory.save_config_path(CONFIG_DIR)
    config_path = os.path.join(base_dir, CONFIG_FILE)

    with open(config_path) as ark_config:
        bits = ark_config.read()

    config = json.loads(bits)

    if 'anki_db' not in config:
        raise KeyError

    return config
