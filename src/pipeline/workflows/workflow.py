from langraph.graph import StateGraph, START, END
from src.pipeline.state.data_state import MyState
from src.pipeline.nodes.nodes import Nodes
node_instance = Nodes()
classification_node = node_instance.classification_node
extraction_node = node_instance.extraction_node

agent_builder = StateGraph(MyState)

agent_builder.add_node("classification_node", classification_node)
agent_builder.add_node("extraction_node",  extraction_node)


agent_builder.add_edge(START,'classification_node')
agent_builder.add_edge('classification_node','extraction_node')
agent_builder.add_edge('extraction_node',END)

graph = agent_builder.compile()
