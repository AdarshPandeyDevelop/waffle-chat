# 🧠 Waffle Chat

A minimalist, conversational AI chat interface powered by **DeepSeek-R1-0528** — a state-of-the-art reasoning model — built with LangChain and Streamlit. Waffle Chat exposes the model's internal chain-of-thought ("thinking") as an optional, toggleable panel alongside the final response.

---

## ✨ Features

- 💬 **Multi-turn conversation** — maintains full chat history across turns using LangChain's message passing
- 🧠 **Reasoning transparency** — toggle the model's `<think>` block to see *how* it arrived at an answer
- ⚡ **Inference via HuggingFace Endpoint** — no local GPU required; uses HuggingFace's Inference API
- 🗑️ **Clear conversation** — one-click reset from the sidebar
- 🎯 **Clean, minimal UI** — centered layout with a distraction-free chat interface
- 🔒 **Environment-based secrets** — API keys managed via `.env`, never hardcoded

---

## 🖼️ Preview

> Chat interface with optional reasoning panel:

```
┌─────────────────────────────────────────────┐
│  🧠 Waffle          │  💬 Chat              │
│  Model: DeepSeek    │                       │
│  ─────────────────  │  You: Explain GRPO    │
│  [Show reasoning]   │                       │
│  ─────────────────  │  💭 Reasoning ▼       │
│  Messages: 4        │   (thinking steps...) │
│  [🗑️ Clear]        │                       │
│                     │  Assistant: GRPO is.. │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| **LLM** | `deepseek-ai/DeepSeek-R1-0528` via HuggingFace |
| **LLM Framework** | LangChain (`langchain-huggingface`) |
| **UI** | Streamlit |
| **Secrets** | `python-dotenv` |
| **Parsing** | Python `re` (regex for `<think>` extraction) |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/waffle-chat.git
cd waffle-chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your HuggingFace API key

Create a `.env` file in the project root:

```env
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
```

I'm not uploading the API Token due to privacy and security concerns, if you want to run it, please get your own Access token from Huggingface, it's easy to get one and then you'll have to create .env file and paste the token as instructed above and it will work perfectly. Thank you!

> Get your token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens). Make sure it has **read** access.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## ⚙️ How It Works

### Model Loading
The model is loaded once and cached using `@st.cache_resource`, so it isn't reloaded on every Streamlit rerun:

```python
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    llm = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-R1-0528", ...)
    return ChatHuggingFace(llm=llm)
```

### Reasoning Extraction
DeepSeek-R1 wraps its chain-of-thought inside `<think>...</think>` tags before giving the final answer. The `extract_response()` function separates these two parts using regex:

```python
def extract_response(content: str):
    """Returns (think_text, final_text)."""
    think_match = re.search(r"<think>(.*?)</think>", content, flags=re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""
    cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return think_text, cleaned
```

### Conversation History
The full message history is stored in `st.session_state.lc_history` as a plain list of strings (alternating user and assistant turns), and passed directly to `model.invoke()` on each turn to maintain context.

---

## 🔧 Configuration

You can tune the model's behavior by editing these parameters inside `load_model()` in `app.py`:

| Parameter | Default | Description |
|---|---|---|
| `max_new_tokens` | `2048` | Max tokens in the response |
| `do_sample` | `False` | Greedy decoding (deterministic) |
| `repetition_penalty` | `1.03` | Penalizes repeated phrases |
| `provider` | `"auto"` | HuggingFace inference provider |

---

## 📦 Dependencies

```
langchain
langchain-core
langchain-openai
langchain-anthropic
langchain-google-genai
langchain-huggingface
transformers
huggingface-hub
google-generativeai
openai
python-dotenv
numpy
scikit-learn
streamlit
```

> Note: `langchain-openai`, `langchain-anthropic`, and `langchain-google-genai` are included for future extensibility (easy model switching). Only HuggingFace is used by default.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 👤 Author

**Adarsh**
- GitHub: https://github.com/AdarshPandeyDevelop
- Built as part of a hands-on LangChain + GenAI learning journey 🚀
