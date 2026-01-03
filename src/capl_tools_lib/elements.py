from enum import Enum
from typing import List, Optional, Any

class CAPLElement:
    def __init__(self, name: str, start_line: int, end_line: int, signature: Optional[str] = None):
        self.name = name
        self.start_line = start_line   # 0-indexed
        self.end_line   = end_line     # 0-indexed
        self.signature  = signature
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, start_line={self.start_line}, end_line={self.end_line}, signature={self.signature})"
    
    def get_line_range(self) -> tuple[int, int]:
        return (self.start_line, self.end_line)
    
class TestCase(CAPLElement):
    def __init__(self, name: str, description: str, start_line: int, end_line: int, group: Optional[str] = None):
        super().__init__(name, start_line, end_line, signature=f"testcase {name}()")
        self.description: str     = description
        self.group: Optional[str] = group

class Handler(CAPLElement):
    def __init__(self, name: str, event_type: str, condition: str, start_line: int, end_line: int, signature: Optional[str] = None):
        super().__init__(name, start_line, end_line, signature=signature or f"on {event_type} {condition}")
        self.event_type: str = event_type
        self.condition: str  = condition

class Function(CAPLElement):
    def __init__(self, name: str, return_type: str, parameters: List[str], start_line: int, end_line: int, signature: Optional[str] = None):
        super().__init__(name, start_line, end_line, signature=signature or f"{return_type} {name}({', '.join(parameters)})")
        self.return_type: str     = return_type
        self.parameters: List[str] = parameters

    def __repr__(self) -> str:
        return f"Function({self.return_type} {self.name} ({self.parameters}), lines {self.start_line}-{self.end_line})"

class TestFunction(CAPLElement):
    def __init__(self, name: str, params: List[str], start_line: int, end_line: int, signature: Optional[str] = None):
        super().__init__(name, start_line, end_line, signature=signature or f"testfunction {name}({', '.join(params)})")
        self.params: List[str] = params

    def __repr__(self) -> str:
        return f"TestFunction({self.name} ({self.params}), lines {self.start_line}-{self.end_line})"
    
class CaplInclude(CAPLElement):
    def __init__(self, included_files: list[str], start_line: int, end_line: int):
        self.included_files: list[str] = included_files
        self.start_line: int = start_line
        self.end_line: int = end_line


    def __repr__(self) -> str:
        return f"CaplIncludes(files = {self.included_files}, lines {self.start_line}-{self.end_line})"

class CaplVariable(CAPLElement):
    def __init__(self,start_line: int, end_line: int):
        super().__init__(name="Variables", start_line=start_line, end_line=end_line,signature="variables {...}")

    def __repr__(self) -> str:
        return f"CaplVariable(lines = {self.start_line}-{self.end_line})"