from typing import TypedDict, Dict, Any

class AgentState(TypedDict):
    email: str
    iocs: Dict[str, Any]
    threat: Dict[str, Any]
    memory: Dict[str, Any]
    reasoning: Dict[str, Any]
    verdict: str
    risk_score: int