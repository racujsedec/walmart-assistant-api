import os
from pathlib import Path
from anthropic import AsyncAnthropic
SYSTEM = (Path(__file__).parent / "prompts" / "system.txt").read_text(encoding="utf-8")
TOOLS = [{"name":"get_order_status", "description":"Retrieve the current status and estimated delivery date for an order ID.","input_schema":{"type":"object","properties":{"order_id":{"type":"string","description":"Numeric order identifier"}},"required":["order_id"]}}]
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "missing-key"))
async def ask_claude(messages):
    return await client.messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"), max_tokens=600, system=SYSTEM, tools=TOOLS, messages=messages)
