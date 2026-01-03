import logging
from pathlib import Path
from common import get_logger
TEST_STATUS_PASS = 1
TEST_STATUS_FAIL = 0
TEST_STATUS_SKIPPED = -2
TEST_STATUS_INCONCLUSIVE = -3

logger = get_logger(__name__)

class CaplFileManager:
    """ 
    Handles Low Level file operations for CAPL files, reading, writing, and managing file paths.
    """
    def __init__(self, file_path: Path):
        self.file_path: Path = file_path
        self.lines: list[str] = []

        logger.debug(f"Initialized CaplFileManager for {file_path}")
        self._read_file()

    def _read_file(self):
        try:
            with self.file_path.open('r', encoding='cp1252') as f:
                self.lines = f.readlines()
                logger.debug(f"Successfully read {len(self.lines)} lines from {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading {self.file_path}: {e}")
            raise IOError(f"Could not read file {self.file_path}: {e}")

    def get_lines(self, start: int, end: int) -> list[str]:
        if start < 0 or end > len(self.lines) or start >= end:
            logger.error(f"Invalid line range requested: {start} to {end}")
            raise ValueError(f"Invalid line range: {start} to {end}")
        
        logger.debug(f"Retrieving lines {start} to {end} from {self.file_path}")
        
        return self.lines[start:end]