import streamlit as st
from agent_mcp import MCPGeminiAgent
from constants import API_KEY

st.set_page_config(page_title="🧠 Gemini LangChain-Style Agent", layout="wide")
st.title("🤖 Gemini Agent with LangChain-style Tools & Memory")

# Initialize agent once
if "agent" not in st.session_state:
    st.session_state.agent = MCPGeminiAgent(api_key=API_KEY)

agent = st.session_state.agent

# ✅ MANUAL TEXT INPUT
user_input = st.text_area("💬 Your message:", height=150)
if st.button("Send"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            reply = agent.run(user_input)
            st.markdown("**🤖 Gemini says:**")
            if reply.strip().startswith("```"):
                st.markdown(reply, unsafe_allow_html=True)
            elif "Code executed successfully" in reply or reply.startswith("❌ Error"):
                st.code(reply, language="python")
            else:
                st.markdown(reply)

# ✅ FILE UPLOADER BLOCK (Insert here)
uploaded_file = st.file_uploader("📄 Upload PDF or DOCX file", type=["pdf", "docx"])
if uploaded_file is not None:
    filepath = f"temp_{uploaded_file.name}"
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Uploaded {uploaded_file.name}")
    
    # Auto-invoke readfile tool
    command = f"readfile {filepath}"
    with st.spinner("Reading file..."):
        result = agent.run(command)
        st.markdown("**📝 Extracted Text:**")
        st.markdown(result)

# ✅ CONVERSATION MEMORY
with st.expander("🧠 Memory"):
    for role, msg in agent.get_history():
        st.markdown(f"**{role.capitalize()}**: {msg}")
