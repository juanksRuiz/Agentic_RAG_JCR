# wrap a python function to do anything I want as a tool I can provide to agent
from langchain_core.tools import tool

@tool
def note_tool(note):
    """
    Describe here what the tool actually does and how to access the tool
    
    Example:
    saves a note to a local file:

    Args:
        note: the text note to save
    """
    with open("notes.txt", "a") as f:
        f.write(note + "\n")