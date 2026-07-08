"""
==========================================================
Blockchain Staking Analytics

Logging Configuration

Creates both console and file logging.

Author: Babacar Ba
==========================================================
"""

import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("staking_etl")
logger.setLevel(logging.INFO)

# Prevent duplicate log messages
logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Log to file
file_handler = logging.FileHandler("logs/pipeline.log")
file_handler.setFormatter(formatter)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)