import json
import logging
import httpx
from typing import TypedDict
from langgraph.graph import StateGraph, END
from .claude_client import ask_claude
from .order_tool import get_order_status
from pydantic import ValidationError
logger = logging.getLogger(__name__)
class State(TypedDict):
    messages: list
    permissions: list[str]
    answer: str
    requested_tools: list
async def agent(state: State):
    response = await ask_claude(state["messages"])
    blocks = []
    requested = []
    for b in response.content:
        if b.type == "text": blocks.append({"type":"text", "text":b.text})
        elif b.type == "tool_use":
            blocks.append({"type":"tool_use", "id":b.id,"name":b.name,"input":b.input})
            requested.append({"id":b.id,"name":b.name,"input":b.input})
    answer = " ".join(b["text"] for b in blocks if b["type"] == "text")
    return {"messages":state["messages"] + [{"role":"assistant","content":blocks}], "requested_tools":requested,"answer":answer}
async def tools_node(state: State):
    results=[]
    for call in state["requested_tools"]:
        if call["name"] != "get_order_status":
            data={"error":"UNKNOWN_TOOL"}
        else:
            try:
                data=await get_order_status(call["input"].get("order_id", ""), state["permissions"])
            except ValidationError:
                data={"error":"INVALID_ORDER_ID"}
            except httpx.HTTPStatusError as e:
                data={"error":"ORDER_NOT_FOUND" if e.response.status_code == 404 else "ORDER_API_ERROR"}
            except (httpx.RequestError, KeyError, ValueError):
                logger.exception("Order lookup failed")
                data={"error":"ORDER_API_UNAVAILABLE"}
        results.append({"type":"tool_result", "tool_use_id":call["id"],"content":json.dumps(data)})
    return {"messages":state["messages"] + [{"role":"user","content":results}],"requested_tools":[]}
def route(state: State):
    return "tools" if state["requested_tools"] else "end"
builder=StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", tools_node)
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", route, {"tools":"tools","end":END})
builder.add_edge("tools", "agent")
graph=builder.compile()
