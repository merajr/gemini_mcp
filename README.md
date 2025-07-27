# 🤖 Gemini MCP Agent – Modular Tool-Using AI in Streamlit

This project is a LangChain-style, [Model Context Protocol (MCP)](https://smith.langchain.com/hub/langchain/MCP) compliant AI agent built on **Google Gemini Pro**, supporting dynamic tools, code execution, file reading, and more — all inside a clean Streamlit app.

---

## Screen Shots

<img width="1783" height="824" alt="image" src="https://github.com/user-attachments/assets/2bf3d719-8f14-484f-8a74-37bcaac54a90" />


## 🚀 Features

✅ Gemini Pro API integration  
✅ MCP-style prompt + tool schema injection  
✅ Agent runtime with plan → act → observe loop  
✅ Tool output formatted in Markdown/code blocks  
✅ Dynamic tool discovery (just drop in new files)  
✅ Built-in tools:
- 📄 `readfile` → PDF/DOCX parser
- 🌐 `scrape` → web page content extractor
- 📚 `wikipedia` → 3-sentence topic summary
- 🧮 `code` → secure Python code execution

---

## 🧠 Architecture Overview

```
User Prompt → Streamlit UI → MCP Agent
           ↘︎ Memory ↘︎ Tool Schemas ↘︎
        → Gemini Pro API → JSON response → Tool call / Final Answer
```

| Layer              | Implementation                     |
|-------------------|-------------------------------------|
| LLM API           | Gemini via `google.generativeai`    |
| Prompt Pipeline   | MCP format with tool schema JSON    |
| Agent Runtime     | Custom loop: plan → act → observe   |
| Orchestration     | Modular Streamlit + dynamic tools   |

---

## 🛠️ Tools Directory

All tools inherit from `BaseTool` and live in `tools/`.

Tool schema auto-discovery is handled dynamically — no need to manually register.

To add a new tool:

```python
# tools/my_tool.py

from tools.base_tool import BaseTool

class MyTool(BaseTool):
    name = "mytool"
    description = "Do something useful"
    parameters = {
        "type": "object",
        "properties": {"input": {"type": "string", "description": "Some input"}},
        "required": ["input"]
    }

    def run(self, **kwargs) -> str:
        return f"You said: {kwargs['input']}"
```

---

## 🖥️ How to Run

### 1. Clone the repo and install requirements

```bash
git clone https://github.com/yourname/gemini-mcp-agent.git
cd gemini-mcp_agent
pip install -r requirements.txt
```

### 2. Set your Gemini API key

In `app.py`, replace:

```python
API_KEY = "YOUR_API_KEY_HERE"
```

with your actual key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

Or load it from `.env`.

---

### 3. Run the app

```bash
streamlit run app.py
```

---

## 💬 Example Prompts

- `Wikipedia: Isaac Newton`
- `Scrape https://www.example.com`
- `Upload a file, then say: Summarize this document`
- `What is 32 * 17?`
- `Use code to compute factorial of 5`

---

## 🧩 Coming Next?

- [ ] `.eml` email file parsing
- [ ] Vector memory / RAG from file chunks
- [ ] FastAPI deployment backend
- [ ] LangGraph-style multi-agent workflows

---

## 📄 License

MIT — free to use, modify, and extend.

---

## 🙌 Acknowledgments

- [Google Generative AI SDK](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [LangChain MCP Protocol](https://smith.langchain.com/hub/langchain/MCP)

---

> Built with ❤️ to explore agentic LLMs and modular AI design.
