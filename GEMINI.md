## CaplEditor Class

### Overview
The `CaplEditor` class handles modification of CAPL file content, providing methods for deleting, inserting, and replacing lines and elements.

### Usage
```python
from capl_tools_lib.core import CaplFileManager
from capl_tools_lib.editor import CaplEditor

# Initialize with a CaplFileManager instance
file_manager = CaplFileManager("path/to/file.can")
editor = CaplEditor(file_manager)

# Remove specific elements
elements_to_remove = [element1, element2]
editor.remove_elements(elements_to_remove)

# Insert new content
new_lines = ["void newFunction() {", "  // implementation", "}"]
editor.insert_element(position=10, element_lines=new_lines)

# Replace existing content
editor.replace_lines(start=5, end=8, lines=["// new content"])
```

### Key Methods

#### Line Operations
- `delete_lines(start: int, end: int)` - Deletes lines from start (inclusive) to end (exclusive)
- `insert_lines(position: int, lines: List[str])` - Inserts lines at specified position
- `replace_lines(start: int, end: int, lines: List[str])` - Replaces a range of lines

#### Element Operations
- `remove_element(element: CAPLElement)` - Removes a single CAPL element
- `remove_elements(elements: List[CAPLElement])` - Removes multiple elements (sorted by line number)
- `insert_element(position: int, element_lines: List[str])` - Inserts a new element

#### Utility Methods
- `_get_modified_lines()` - Returns current modified content as list of lines
- Internal copy of file lines maintained for modification tracking

### Important Notes

**Index Handling:**
- All line indices are 0-indexed
- `delete_lines` and `replace_lines` use exclusive end index (Python slice convention)
- `CAPLElement.end_line` is inclusive, so +1 is added when calling `delete_lines`

**Element Removal:**
- Elements are automatically sorted by start line in descending order
- This prevents index shifting issues when removing multiple elements

**Validation:**
- All methods validate line ranges and positions
- Invalid ranges raise `ValueError` with descriptive messages
- Comprehensive logging for all operations

### Example: Batch Element Removal
```python
# Remove multiple test cases
test_cases = file_manager.get_test_cases()
obsolete_tests = [tc for tc in test_cases if "deprecated" in tc.name.lower()]

editor = CaplEditor(file_manager)
editor.remove_elements(obsolete_tests)

# Get modified content
modified_lines = editor._get_modified_lines()
```

### Design Considerations

1. **Non-destructive**: Works on a copy of original lines
2. **Logging**: All operations logged for debugging
3. **Error handling**: Validates all inputs before modification
4. **Batch operations**: Efficiently handles multiple element removals