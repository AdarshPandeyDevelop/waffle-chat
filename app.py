from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st
import re
load_dotenv()
st.set_page_config(
    page_title="Waffle Chat",
    page_icon="🧠",
    layout="centered",
)
# ── Model loader


@st.cache_resource(show_spinner="Loading model...")
def load_model():
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-R1-0528",
        task="text-generation",
        max_new_tokens=2048,
        do_sample=False,
        repetition_penalty=1.03,
        provider="auto",
    )
    return ChatHuggingFace(llm=llm)
# ── Helper


def extract_response(content: str):
    """Returns (think_text, final_text)."""
    think_match = re.search(r"<think>(.*?)</think>", content, flags=re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""
    cleaned = re.sub(r"<think>.*?</think>", "",
                     content, flags=re.DOTALL).strip()
    if not cleaned:
        cleaned = think_text
    return think_text, cleaned


# ── Session state
if "messages" not in st.session_state:
    # Each entry: {"role": "user"|"assistant", "content": str, "think": str}
    st.session_state.messages = []
if "lc_history" not in st.session_state:
    # Raw strings passed to LangChain
    st.session_state.lc_history = []
# ── Sidebar
with st.sidebar:
    st.title("🧠 Waffle")
    st.caption("Model: `deepseek-ai/DeepSeek-R1-0528`")
    st.divider()
    show_thinking = st.toggle("Show reasoning (thinking)", value=False)
    st.divider()
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_history = []
        st.rerun()
    st.divider()
    st.caption("Built with LangChain + HuggingFace")
# ── Page title
st.title("💬 Chat")
# ── Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("think") and show_thinking:
            with st.expander("💭 Reasoning", expanded=False):
                st.markdown(msg["think"])
        st.markdown(msg["content"])
# ── Chat input
if prompt := st.chat_input("Ask Waffle..."):
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "think": ""})
    st.session_state.lc_history.append(prompt)
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            model = load_model()
            result = model.invoke(st.session_state.lc_history)
            think, final = extract_response(result.content)
        if think and show_thinking:
            with st.expander("💭 Reasoning", expanded=False):
                st.markdown(think)
        st.markdown(final)
    st.session_state.lc_history.append(result.content)
    st.session_state.messages.append({
        "role": "assistant",
        "content": final,
        "think": think,
    })
