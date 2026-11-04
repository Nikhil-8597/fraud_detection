from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
import operator

class MyState(TypedDict):
    message : Annotated[list[AnyMessage], operator.add]
    doc_url : str
    prompt : str
    doc_type : str
