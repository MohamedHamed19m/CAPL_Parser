import pytest
from capl_tools_lib.processor import CaplProcessor

@pytest.fixture
def complex_can_file(tmp_path):

    """Create a temporary .can file with various elements."""
    file_path = tmp_path / "complex.can"
    content = [
        "includes {\n",
        "}\n",
        "variables {\n",
        "  int gVar = 0;\n",
        "}\n",
        "on key 'a' {\n",
        '  write("key a pressed");\n',
        "}\n",
        "on timer t1 {\n",
        '  write("timer t1 expired");\n',
        "}\n",
        "testcase TC1() {\n",
        '  InitializeTestGroup("GroupA");\n',
        "}\n",
    ]
    file_path.write_text("".join(content), encoding="cp1252")
    return file_path


def test_insert_section_alias_include(complex_can_file):
    """Test 'include' as alias for 'includes'."""
    processor = CaplProcessor(complex_can_file)
    result = processor.insert(
        location="section:include", code_string='#include "test.cin"'
    )
    assert result is True
    processor.save()

    content = complex_can_file.read_text(encoding="cp1252")
    assert '#include "test.cin"' in content


def test_insert_section_alias_variable(complex_can_file):
    """Test 'variable' as alias for 'variables'."""
    processor = CaplProcessor(complex_can_file)
    result = processor.insert(
        location="section:variable", code_string="byte new_byte = 0xFF;"
    )
    assert result is True
    processor.save()

    content = complex_can_file.read_text(encoding="cp1252")
    assert "byte new_byte = 0xFF;" in content


def test_insert_after_handler_key(complex_can_file):
    """Test inserting after an 'on key' handler."""
    processor = CaplProcessor(complex_can_file)
    # The name should be exactly what the scanner produces: "on key 'a'"
    result = processor.insert(
        location="after:on key 'a'", code_string="void NewFunc() {}"
    )
    assert result is True
    processor.save()

    content = complex_can_file.read_text(encoding="cp1252")
    assert "void NewFunc() {}" in content
    # Ensure it's after the key handler
    lines = content.splitlines()
    handler_found = False
    func_found = False
    for line in lines:
        if "on key 'a'" in line:
            handler_found = True
        if "void NewFunc() {}" in line and handler_found:
            func_found = True
            break
    assert func_found


def test_insert_after_handler_timer(complex_can_file):
    """Test inserting after an 'on timer' handler."""
    processor = CaplProcessor(complex_can_file)
    result = processor.insert(
        location="after:on timer t1", code_string="// Comment after timer"
    )
    assert result is True
    processor.save()

    content = complex_can_file.read_text(encoding="cp1252")
    assert "// Comment after timer" in content


def test_insert_error_message_with_suggestions(complex_can_file):
    """Test that error message includes available sections/groups."""
    processor = CaplProcessor(complex_can_file)
    with pytest.raises(ValueError) as excinfo:
        processor.insert(location="section:NonExistent", code_string="// test")

    error_msg = str(excinfo.value)
    assert "Section or Group 'NonExistent' not found" in error_msg
    assert "Available: includes, variables, GroupA" in error_msg


def test_insert_strip_location(complex_can_file):
    """Test that whitespace in location is stripped."""
    processor = CaplProcessor(complex_can_file)
    # Extra spaces around section name
    result = processor.insert(
        location="section:  include  ", code_string="// stripped test"
    )
    assert result is True
    processor.save()

    content = complex_can_file.read_text(encoding="cp1252")
    assert "// stripped test" in content
