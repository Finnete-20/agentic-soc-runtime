from typing import TypedDict, Dict, Any

class AgentState(TypedDict):
    email: str
    iocs: Dict[str, Any]
    reasoning: Dict[str, Any]
    result: Dict[str, Any]