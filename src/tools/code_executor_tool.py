from tools.base_tool import BaseTool
import contextlib
import io


class CodeExecutorTool(BaseTool):
    name = "code"
    description = "Execute simple Python code and return the result or printed output."
    parameters = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute"}
        },
        "required": ["code"]
    }

    def run(self, **kwargs) -> str:
        code = kwargs["code"]

        # Define a safe subset of built-ins
        safe_builtins = {
            "print": print,
            "len": len,
            "range": range,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "sorted": sorted
        }

        safe_globals = {"__builtins__": safe_builtins}
        safe_locals = {}

        # Capture print() output
        import io, contextlib
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(code, safe_globals, safe_locals)
            output = stdout.getvalue()
            return f"```python\n{output.strip()}\n```" if output else "✅ Code executed successfully (no output)."
        except Exception as e:
            return f"```python\n❌ Error: {e}\n```"
