from langgraph.graph import StateGraph,END
from app.agents.state import AgentState
from app.agents.nodes.supervisor import call_claude
from app.agents.nodes.execute_tools import execute_tools
def route(state:AgentState)->str:return 'tools' if state.get('requested_tools') else 'end'
builder=StateGraph(AgentState)
builder.add_node('agent',call_claude)
builder.add_node('tools',execute_tools)
builder.set_entry_point('agent')
builder.add_conditional_edges('agent',route,{'tools':'tools','end':END})
builder.add_edge('tools','agent')
# No fake FirestoreSaver. This graph runs per request; durable checkpoints require an adapter.
graph=builder.compile()
