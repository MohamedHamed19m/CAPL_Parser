import sys
import os

# Add src to path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import logging
from capl_tools_lib.common import get_logger, MODULE_CONFIG

# --- Simulate User Configuration ---
# Let's say we want to debug the 'scanner' but keep 'parser' quiet.
MODULE_CONFIG["capl_tools_lib.scanner"] = logging.DEBUG
# 'capl_tools_lib.parser' is not in config, so it gets DEFAULT_LEVEL (WARNING)

# --- Simulate Module Usage ---

# 1. Scanner Module (Enabled for DEBUG)
scanner_logger = get_logger("capl_tools_lib.scanner")
print("--- Testing Scanner (DEBUG enabled) ---")
scanner_logger.debug("This is a DEBUG message from scanner (Visible)")
scanner_logger.info("This is an INFO message from scanner (Visible)")

# 2. Parser Module (Default: WARNING)
parser_logger = get_logger("capl_tools_lib.parser")
print("\n--- Testing Parser (Default: WARNING) ---")
parser_logger.debug("This is a DEBUG message from parser (Hidden)")
parser_logger.info("This is an INFO message from parser (Hidden)")
parser_logger.warning("This is a WARNING message from parser (Visible)")
