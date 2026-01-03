# CAPL Tools Library Documentation

## CaplScanner Class

### Overview
The `CaplScanner` is the primary entry point for analyzing CAPL files. It uses a modular strategy pattern (`CaplScanningStrategy`) to parse different CAPL constructs like includes, variables, handlers, functions, and test cases.

### Usage
```python
from capl_tools_lib.core import CaplFileManager
from capl_tools_lib.scanner import CaplScanner

file_manager = CaplFileManager("path/to/file.can")
scanner = CaplScanner(file_manager)

# Scan for all supported elements
all_elements = scanner.scan_all()
```

### Scanning Strategies

The scanner delegates work to specialized strategy classes, making it easy to extend:

1.  **IncludesScanner**:
    -   Finds `#include "..."` directives inside `includes { ... }` blocks.
2.  **VariablesScanner**:
    -   Identifies the global `variables { ... }` block.
3.  **HandlerScanner**:
    -   Parses event handlers like `on message ...`, `on timer ...`, `on start`.
    -   *Note*: Ignores statements that look like handlers but end in `;` (e.g. inside other functions).
4.  **TestCaseScanner**:
    -   Specifically finds `testcase Name() { ... }` blocks.
5.  **FunctionScanner**:
    -   Finds `testfunction` definitions.
    -   Finds standard CAPL functions (e.g., `void func(int a)`).

### Extensibility

To add support for a new CAPL construct:
1.  Create a new class inheriting from `CaplScanningStrategy`.
2.  Implement the `scan(file_manager)` method.
3.  Define a class-level regex `PATTERN`.
4.  Add the new strategy to `CaplScanner.strategies` list.

---

## CaplEditor Class

### Overview
The `CaplEditor` class handles modification of CAPL file content, providing methods for deleting, inserting, and replacing lines and elements. It works on a copy of the original file content, allowing non-destructive editing operations.

### Usage

#### Basic Setup
```python
from capl_tools_lib.core import CaplFileManager
from capl_tools_lib.editor import CaplEditor

# Initialize with a CaplFileManager instance
file_manager = CaplFileManager("path/to/file.can")
editor = CaplEditor(file_manager)
```

#### Removing Elements
```python
# Remove a single element
editor.remove_element(element)

# Remove multiple elements
elements_to_remove = [element1, element2, element3]
editor.remove_elements(elements_to_remove)
```

#### Inserting Content
```python
# Insert new lines at a specific position
new_lines = [
    "void newFunction() {",
    "  // implementation",
    "}"
]
editor.insert_element(position=10, element_lines=new_lines)
```

#### Replacing Content
```python
# Replace a range of lines
editor.replace_lines(start=5, end=8, lines=["// new content"])

# Replace an entire element
new_implementation = [
    "void updatedFunction() {",
    "  // new implementation",
    "}"
]
editor.replace_element(element, new_lines=new_implementation)
```

#### Saving Changes
```python
# Save to original file (with backup)
editor.save(backup=True)

# Save to a new file
editor.save(output_path=Path("modified_file.can"))

# Get content as string without saving
content = editor.get_content()
```

### Key Methods

#### Line Operations
- **`delete_lines(start: int, end: int)`** - Deletes lines from start (inclusive) to end (exclusive)
- **`insert_lines(position: int, lines: List[str])`** - Inserts lines at specified position
- **`replace_lines(start: int, end: int, lines: List[str])`** - Replaces a range of lines

#### Element Operations
- **`remove_element(element: CAPLElement)`** - Removes a single CAPL element
- **`remove_elements(elements: List[CAPLElement])`** - Removes multiple elements (sorted by line number)
- **`insert_element(position: int, element_lines: List[str])`** - Inserts a new element
- **`replace_element(element: CAPLElement, new_lines: List[str])`** - Replaces an existing element

#### File Operations
- **`save(output_path: Optional[Path] = None, backup: bool = True)`** - Saves modified content to file
- **`reset()`** - Resets all modifications back to original content

#### Utility Methods
- **`get_content()`** - Returns current modified content as a single string
- **`get_line_count()`** - Returns the current number of lines
- **`get_lines(start: int, end: int)`** - Gets a range of lines
- **`_get_modified_lines()`** - Returns current modified content as list of lines (internal)

### Important Notes

#### Index Handling
- All line indices are **0-indexed**
- `delete_lines` and `replace_lines` use **exclusive end index** (Python slice convention)
- `CAPLElement.end_line` is **inclusive**, so `+1` is added when calling `delete_lines`

**Example:**
```python
# Element spans lines 10-12 (inclusive in CAPLElement)
element.start_line = 10
element.end_line = 12

# When deleting, add 1 to make end exclusive
editor.delete_lines(10, 13)  # Deletes lines 10, 11, 12
```

#### Element Removal
- Elements are **automatically sorted by start line in descending order**
- This prevents index shifting issues when removing multiple elements
- Editing happens from bottom to top of the file

#### Validation
- All methods validate line ranges and positions
- Invalid ranges raise `ValueError` with descriptive messages
- Comprehensive logging for all operations

### Examples

#### Example 1: Batch Element Removal
```python
# Remove multiple test cases
test_cases = file_manager.get_test_cases()
obsolete_tests = [tc for tc in test_cases if "deprecated" in tc.name.lower()]

editor = CaplEditor(file_manager)
editor.remove_elements(obsolete_tests)
editor.save(backup=True)
```

#### Example 2: Replace Handler Implementation
```python
from capl_tools_lib.scanner import CaplScanner

# Find specific handler
scanner = CaplScanner(file_manager)
handlers = scanner.scan_all()
on_start_handler = next(h for h in handlers if "on start" in h.signature)

# Replace with new implementation
new_handler = [
    "on start {",
    "  write('System initialized');",
    "  initializeTimers();",
    "}"
]

editor = CaplEditor(file_manager)
editor.replace_element(on_start_handler, new_handler)
editor.save()
```

#### Example 3: Insert New Function
```python
# Insert a new function after line 50
new_function = [
    "",
    "void logMessage(char msg[]) {",
    "  write('[LOG] ' + msg);",
    "}",
    ""
]

editor = CaplEditor(file_manager)
editor.insert_element(position=50, element_lines=new_function)
editor.save()
```

#### Example 4: Preview Changes Without Saving
```python
editor = CaplEditor(file_manager)
editor.remove_elements(obsolete_elements)

# Preview changes
modified_content = editor.get_content()
print(modified_content)

# Decide not to save
editor.reset()  # Revert all changes
```

### Design Considerations

1. **Non-destructive**: Works on a copy of original lines - original file untouched until `save()` is called
2. **Automatic backup**: Optional backup file creation (`.bak` extension) when overwriting
3. **Logging**: All operations logged for debugging and audit trail
4. **Error handling**: Validates all inputs before modification
5. **Batch operations**: Efficiently handles multiple element removals with automatic sorting
6. **Flexible output**: Save to new file, overwrite original, or just get the modified content

### Integration with CaplScanner

The `CaplEditor` is designed to work seamlessly with elements discovered by `CaplScanner`:

```python
from capl_tools_lib.core import CaplFileManager
from capl_tools_lib.scanner import CaplScanner
from capl_tools_lib.editor import CaplEditor

# Scan file
file_manager = CaplFileManager("test.can")
scanner = CaplScanner(file_manager)
elements = scanner.scan_all()

# Filter elements to remove
test_cases = [e for e in elements if isinstance(e, TestCase)]
failed_tests = [tc for tc in test_cases if tc.name.startswith("FAIL_")]

# Edit file
editor = CaplEditor(file_manager)
editor.remove_elements(failed_tests)
editor.save(output_path=Path("cleaned_test.can"))
```

---

## CaplFileManager Class

### Overview
The `CaplFileManager` class provides file reading and line management capabilities for CAPL files.

### Usage
```python
from capl_tools_lib.core import CaplFileManager

file_manager = CaplFileManager("path/to/file.can")

# Access file content
lines = file_manager.lines
file_path = file_manager.file_path
```

### Key Features
- Reads CAPL files with UTF-8 encoding
- Provides access to file lines as a list
- Maintains file path reference
- Handles file reading errors gracefully



## Development Environment Setup

### Critical Configuration Rules

#### 1. Build System Configuration
**DO NOT modify the build system configuration unless absolutely necessary:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- Hatchling **automatically discovers** packages in `src/` directory
- **DO NOT add** `[tool.hatchling.build.targets.wheel]` unless you have a non-standard layout
- The package name in PyPI uses hyphens: `capl-tools-lib`
- The import name uses underscores: `capl_tools_lib`
- Hatchling converts hyphens to underscores automatically

#### 2. Package Management
**ALWAYS use uv commands, NEVER use pip directly in this project:**

✅ **Correct:**
```bash
uv add package-name              # Add dependency
uv remove package-name           # Remove dependency
uv sync                          # Sync dependencies
uv run python script.py          # Run script
uv run pytest                    # Run tests
```

❌ **NEVER do this:**
```bash
pip install package-name         # Don't use pip
uv pip install package-name      # Don't use uv pip in projects
python script.py                 # May not use project environment
```

#### 3. Running Code

**Scripts in `tests/`:**
```bash
uv run tests/dev_script.py       # Automatically syncs environment first
```

**Running tests:**
```bash
uv run pytest tests/test_scanner.py -v
uv run pytest                    # Run all tests
```

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError: No module named 'capl_tools_lib'"

**Solution 1 - For pytest:**
Check `pyproject.toml` has:
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
```

**Solution 2 - For scripts:**
Run with `uv run`:
```bash
uv run python my_script.py
```

**Solution 3 - Resync environment:**
```bash
uv sync --reinstall
```

#### Issue: "Package not found" or version conflicts

**Solution:**
```bash
uv lock --upgrade          # Update lockfile
uv sync                    # Sync environment
```

#### Issue: Environment seems corrupted

**Solution:**
```bash
rm -rf .venv/             # Delete environment
uv sync                   # Recreate from lockfile
```

### Adding Dependencies

#### Regular Dependencies
```bash
uv add httpx              # Add to [project.dependencies]
uv add "httpx>=0.27.0"   # With version constraint
```

#### Development Dependencies
```bash
uv add --dev pytest       # Add to [dependency-groups.dev]
uv add --dev ruff         # Add development tools
```
