"""
==========================================================
Blockchain Staking Analytics

Configuration Module

Loads application configuration from environment variables.

Author: Babacar Ba
==========================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables from the project root.
load_dotenv()

# Database configuration dictionary.
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}