from mcp.server.fastmcp import FastMCP
import os

mcp=FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__),"notes.txt")
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     return a + b
# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting (name: str) -> str:
#     return f"Hello, {name}!"

def ensure_notes_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'w') as f:
            f.write("")

@mcp.tool()
def add_note(note: str) -> str:

    """Add a note to the sticky notes."""
    ensure_notes_file()
    with open(NOTES_FILE, 'a') as f:
        f.write(note + "\n")
    return "Note added."

@mcp.tool()
def read_notes() -> str:
    """Read all sticky notes."""
    ensure_notes_file()
    with open(NOTES_FILE, 'r') as f:
        notes = f.read().strip()
    return notes or "No notes available."

@mcp.resource("notes://latest")
def get_latest_note()-> str:
    """Get the latest sticky note."""
    ensure_notes_file()
    with open(NOTES_FILE, 'r') as f:
        notes = f.readlines()
    if notes:
        return notes[-1].strip()
    else:
        return "No notes available."

@mcp.prompt()
def summarize_notes() -> str:
    """Summarize all sticky notes."""
    notes = read_notes()
    if notes == "No notes available.":
        return notes
    summary = f"The sticky notes contain the following items:\n{notes}"
    return summary