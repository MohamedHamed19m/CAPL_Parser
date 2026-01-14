# Usage Examples

This page provides practical examples of how to use `capl_tools`, specifically focusing on workflows optimized for AI agents and automation.

## AI Agent Surgical Workflow

One of the primary use cases for `capl_tools` is allowing an AI agent to modify large CAPL files without needing to read the entire file into its context window. This "surgical" approach saves tokens, prevents errors, and ensures precision.

### 1. Discovery (Low Token Usage)
The agent first maps the file structure to identify the target elements and their semantic locations.

```powershell
capl_tools scan tests/data/sample.can --toon
```

### 2. Context Extraction
The agent fetches only the specific code block it needs to refactor.

```powershell
capl_tools get tests/data/sample.can TC2_MessageHandling --type TestCase
```

### 3. Surgical Replacement
The agent removes the old implementation and inserts the new one directly from a string, eliminating the need for temporary files.

**Step A: Remove the old element**
```powershell
capl_tools remove tests/data/sample.can --type TestCase --name TC2_MessageHandling
```

**Step B: Insert new implementation directly from string**
```powershell
capl_tools insert tests/data/sample.can \
    --location after:TC1_ProcessData \
    --type TestCase \
    --code "testcase TC2_MessageHandling()\n{\n    // Enhanced Logic by AI Agent\n    write('Starting Advanced Message Handling Test...\n');\n    TestStepPass('Initialization', 'Message handlers verified');\n}"
```

### Advanced Insertion with Semantic Anchors

You can also target specialized blocks like includes, variables, or event handlers.

**Insert into global sections using aliases**
```powershell
# Use 'include' as an alias for 'includes'
capl_tools insert test.can --location section:include --code "#include \"CommonLib.cin\""

# Use 'variable' as an alias for 'variables'
capl_tools insert test.can --location section:variable --code "int gGlobalCounter = 0;"
```

**Insert after specific Event Handlers**
Event handlers are identified by their full signature. Use `scan` to find the exact name.
```powershell
# Insert after an 'on key' handler
capl_tools insert test.can --location "after:on key 'a'" --code "void HandleA() { ... }"

# Insert after an 'on timer' handler
capl_tools insert test.can --location "after:on timer MyTimer" --code "// Timer cleanup logic"
```

### 4. Verification
The agent verifies the structure or specific code content to ensure the operation was successful.

```powershell
capl_tools stats tests/data/sample.can
# OR
capl_tools get tests/data/sample.can TC2_MessageHandling --type TestCase
```

## Benefits of this Workflow
- **Context Efficiency**: No need to process thousands of lines of code.
- **Precision**: Semantic anchoring (e.g., `after:FunctionName`) ensures code is placed correctly even if line numbers change.
- **Speed**: Atomic operations using the `--code` flag are faster than full-file rewrites.
- **Reliability**: Minimal disk I/O and no temporary file management.
