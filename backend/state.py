from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    email: str
    iocs: Dict[str, Any]
    threat: Dict[str, Any]
    memory: Dict[str, Any]
    reasoning: Dict[str, Any]
    report: Dict[str, Any]