from typing import TypedDict, Annotated
from langchain_core.messages import Anymessage
import operator

class MyState(TypedDict):
    message : Annotated[list[Anymessage], operator.add]
    doc_url : str
    prompt : str
    doc_type : str
