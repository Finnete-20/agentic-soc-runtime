from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    email_content: str
    extracted_iocs: List[str]
    threat_data: Dict[str, Any]
    risk_score: int
    investigation_steps: List[str]
    final_report: Dict[str, Any]