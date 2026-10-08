from typing import TypedDict,Any
class AgentState(TypedDict,total=False):
 messages:list[dict[str,Any]]
 principal:dict[str,Any]
 requested_tools:list[dict[str,Any]]
 answer:str
 tool_results:list[dict[str,Any]]
 citations:list[dict[str,Any]]
