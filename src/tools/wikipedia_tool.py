from tools.base_tool import BaseTool
import wikipedia, json, inspect

class WikipediaTool(BaseTool):
    name = "wikipedia"
    description = "Search Wikipedia and return a three‑sentence summary."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "topic to look up"}
        },
        "required": ["query"],
    }

    def run(self, **kwargs) -> str:
        try:
            return wikipedia.summary(kwargs["query"], sentences=3)
        except Exception as e:
            return f"Wikipedia error: {e}"
