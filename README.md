# CAPL_Parser

A powerful command-line tool for parsing, analyzing, and manipulating CAPL (CAN Access Programming Language) files.

## Features

- **Parse CAPL Files** – Extract and analyze CAPL code structure
- **Manipulate & Transform** – Modify CAPL code programmatically
- **AST Operations** – Work with abstract syntax trees
- **Validation** – Check CAPL syntax and semantics
- **Code Generation** – Generate CAPL code from templates or specifications

## Installation

```bash
pip install CAPL_Parser
```

Or install from source:

```bash
git clone https://github.com/MohamedHamed19m/CAPL_Parser 
cd CAPL_Parser
pip install -e .
```

## Project Structure

```
capl-forge/
├── src/capl_tools_lib/
│   ├── api.py          # Public API interface
│   ├── core.py         # Core parsing logic
│   ├── editor.py       # Code manipulation utilities
│   ├── elements.py     # CAPL AST element definitions
│   ├── scanner.py      # Lexical analysis
│   └── common.py       # Shared utilities
├── tests/
│   ├── dev_script.py   # Development testing
│   └── data/
│       └── sample.can  # Sample CAPL file
└── README.md
```

## Architecture

**Scanner** → **Parser** → **AST** → **Editor/Transformer** → **Output**

- `scanner.py` – extract 
- `core.py` – Parses 
- `elements.py` – Defines 
- `editor.py` – Provides 
- `api.py` – Exposes 


## Logging

The library includes a flexible logging system that can be configured in `src/capl_tools_lib/common.py`.

### Configuration

Open `src/capl_tools_lib/common.py` to adjust settings:

- **ENABLE_LOGGING**: Master switch to enable/disable all output.
- **DEFAULT_LEVEL**: Default level (e.g., `logging.WARNING`) for all modules.
- **MODULE_CONFIG**: Dictionary to enable specific logging levels for individual files (e.g., `{"capl_tools_lib.scanner": logging.DEBUG}`).

### Usage in Code

```python
from .common import get_logger

logger = get_logger(__name__)

logger.debug("Debug information")
logger.warning("Something might be wrong")
```

## Requirements

- Python 3.11+

## Development with uv

This project uses `uv` for lightning-fast Python package and environment management.

### 1. Initialize and Sync the Environment
Run this in your root directory (`CAPL_Parser`). This command will create the `uv.lock` file and the `.venv` folder.

```powershell
# This reads your pyproject.toml and sets up the virtual environment
uv sync
```

### 2. Run Development Scripts
`uv run` ensures the environment is up to date before executing the script.

```powershell
# Run the demo logging script
uv run tests/demo_logging.py

# Run the dev script
uv run tests/dev_script.py
```

### 3. Adding Dependencies
If you need libraries for your parser (like `lark`, `ply`, or `regex`), add them using:

```powershell
uv add lark
```

### 4. How to use your package in scripts
Because the project uses a `src` layout with `package = true`, `uv` installs the package in editable mode by default. In your scripts, you can simply write:

```python
from capl_tools_lib import core
```

## Contributing

Contributions are welcome! Please submit issues and pull requests.

## Support

For issues and questions, please open an issue on the repository.