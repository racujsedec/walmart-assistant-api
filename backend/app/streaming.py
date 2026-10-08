"""SSE progress example: emits application progress and final answer, not token-by-token Claude streaming."""
import json
from fastapi.responses import StreamingResponse

def event(name, data):
    return f"event: {name}\ndata: {json.dumps(data)}\n\n"

def make_stream(run_workflow):
    async def generator():
        yield event("progress", {"step": "validating"})
        yield event("progress", {"step": "investigating"})
        answer = await run_workflow()
        yield event("final", {"answer": answer})
    return StreamingResponse(generator(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
