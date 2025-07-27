import json, re, google.generativeai as genai
from tools import get_all_tools
from memory import ChatMemory

SYSTEM_TEMPLATE = """You are an AI agent. 
You can either answer directly
  → return: {{"answer": "<text>"}}

OR call a tool
  → return: {{"tool": "<name>", "args": {{...}}}}

TOOLS:
{tool_schemas}

Always return ONLY valid JSON, no extra text."""


def tool_schemas_json(tools):
    return json.dumps(
        {name: {"description": t.description, "parameters": t.parameters}
         for name, t in tools.items()},
        indent=2
    )

class MCPGeminiAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.memory = ChatMemory()
        self.tools = get_all_tools()
        self.system_prompt = SYSTEM_TEMPLATE.format(
            tool_schemas=tool_schemas_json(self.tools)
        )


    def _llm(self, messages: list[str]) -> str:
        prompt = "\n".join(messages)
        resp = self.model.generate_content(prompt)
        return resp.text.strip()

    def _parse_json(self, txt: str):
        try:
            return json.loads(txt)
        except Exception:
            # Try to extract first {...} block
            match = re.search(r"\{.*\}", txt, re.S)
            return json.loads(match.group(0)) if match else {"answer": txt}

    def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)

        while True:
            # 1) build prompt
            convo = "\n".join(f"{r}: {m}" for r, m in self.memory.get_recent())
            llm_input = [self.system_prompt, convo, f"user: {user_input}"]
            llm_reply = self._parse_json(self._llm(llm_input))

            # 2) tool call or final answer?
            if "answer" in llm_reply:
                self.memory.add("gemini", llm_reply["answer"])
                return llm_reply["answer"]

            tool_name = llm_reply.get("tool")
            args = llm_reply.get("args", {})
            if tool_name not in self.tools:
                self.memory.add("gemini", f"Unknown tool {tool_name}")
                return f"❌ Tool `{tool_name}` not available."

            # 3) execute tool
            tool_result = self.tools[tool_name].run(**args)

            # 4) add observation & loop once more
            self.memory.add(tool_name, str(tool_result))
            user_input = f"Observation from {tool_name}: {tool_result}"

    def get_history(self):
        return self.memory.history
