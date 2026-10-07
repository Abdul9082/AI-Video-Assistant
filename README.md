# 🎥 AI Video Assistant

An AI-powered video analysis assistant that transforms YouTube videos and local audio/video files into structured, searchable knowledge.

The application processes video or audio content, transcribes the speech using Whisper, generates AI-powered insights, and creates a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about the processed content.

---

## ✨ Features

- 🎬 **YouTube Video Processing** – Process videos directly from a YouTube URL and extract audio using `yt-dlp`.
- 📁 **Local File Processing** – Process supported local audio/video files.
- 🎙️ **AI Speech-to-Text** – Transcribe audio locally using OpenAI Whisper. Supports English and Hinglish workflows.
- 📝 **AI Summarization** – Generate a concise summary from the transcript.
- 🏷️ **Automatic Title Generation** – Generate a meaningful title based on the video content.
- ✅ **Action Item Extraction** – Identify tasks and action items discussed in the content.
- 💡 **Key Decision Extraction** – Extract important decisions and conclusions.
- ❓ **Open Question Detection** – Identify unresolved or unanswered questions.
- 🧠 **RAG-based Question Answering** – Ask questions about the processed video; relevant transcript sections are retrieved before an answer is generated.
- 🔎 **Semantic Search** – Convert transcript chunks into embeddings for semantic retrieval.
- 🗄️ **Chroma Vector Database** – Store transcript embeddings for RAG-based retrieval.
- 🤖 **Groq LLM Integration** – Generate summaries, insights, and answers using an LLM through Groq.
- 🌐 **Hindi / Hinglish Processing** – Hindi-to-English processing using Sarvam AI.
- 🖥️ **Streamlit Web Interface** – Interactive interface for processing videos and exploring generated insights.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │     User Input      │
                    │ YouTube URL / File  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Audio Processing  │
                    │   yt-dlp / FFmpeg   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Whisper Transcriber │
                    │    Speech → Text    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Transcript      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼─────────────────┐
              │                │                 │
              ▼                ▼                 ▼
       ┌────────────┐   ┌─────────────┐   ┌─────────────┐
       │  Summary   │   │ Information │   │    Title    │
       │ Generation │   │ Extraction  │   │ Generation  │
       └────────────┘   └──────┬──────┘   └─────────────┘
                               │
                     ┌─────────┼─────────┐
                     ▼         ▼         ▼
                  Action    Decisions  Questions
                  Items
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Text Chunking    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ HuggingFace         │
                    │ Embeddings          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    RAG Retrieval    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Groq LLM       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Video Q&A Assistant │
                    └─────────────────────┘
```

---

## 📂 Project Structure

```text
AI-Video-Assistant/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarize.py
│   └── transcriber.py
│
├── utils/
│   └── audio_processor.py
│
├── downloads/        # Generated automatically at runtime
└── vector_db/        # Generated automatically for RAG
```

### Runtime Directories

| Directory | Purpose |
|-----------|---------|
| `downloads/` | Stores downloaded and processed audio files |
| `vector_db/` | Stores the locally generated ChromaDB vector database used by the RAG pipeline |

These directories are excluded from Git using `.gitignore`.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Web application interface |
| yt-dlp | YouTube audio extraction |
| FFmpeg | Audio conversion and processing |
| Pydub | Audio processing |
| OpenAI Whisper | Local speech-to-text transcription |
| LangChain | LLM and RAG orchestration |
| Groq | LLM inference |
| HuggingFace | Text embeddings |
| Sentence Transformers | Embedding generation |
| ChromaDB | Vector database |
| Sarvam AI | Hindi/Hinglish language processing |
| FPDF2 | PDF generation |
| Python-dotenv | Environment variable management |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a Virtual Environment

Using Python:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Or, using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
```

### 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Using uv:

```bash
uv pip install -r requirements.txt
```

---

## 🔧 FFmpeg Setup

FFmpeg is required for audio extraction and conversion.

The Python package `ffmpeg-python` is only a wrapper around FFmpeg. The actual FFmpeg executable must be installed separately and added to your system `PATH`.

Verify the installation:

```bash
ffmpeg -version
```

If FFmpeg is installed correctly, the command will display its version information.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory of the project:

```text
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

The application loads these variables using `python-dotenv`.

> ⚠️ **Security:** Never commit your `.env` file to GitHub.

Your `.gitignore` should contain:

```text
.venv/
__pycache__/
.env
downloads/
vector_db/
.streamlit/secrets.toml
*.pyc
```

---

## ▶️ Running the Application

Using uv:

```bash
uv run streamlit run app.py
```

Or, if your virtual environment is already activated:

```bash
streamlit run app.py
```

Open the URL displayed in the terminal, usually:

```text
http://localhost:8501
```

---

## 🔄 Application Workflow

### Step 1 — Provide Input

The user provides either:

- A YouTube URL
- A supported local audio/video file

### Step 2 — Audio Processing

For YouTube videos, the application uses `yt-dlp` to download the audio. FFmpeg then processes and converts the audio into a format suitable for Whisper.

```text
YouTube URL → yt-dlp → Audio File → FFmpeg → Whisper-compatible Audio
```

### Step 3 — Speech Transcription

The processed audio is passed to OpenAI Whisper, which converts the spoken content into text.

```text
Audio → Whisper → Transcript
```

The transcript becomes the main source of information for the rest of the application.

### Step 4 — Content Analysis

The transcript is processed to generate:

- **Title** – a meaningful title based on the transcript
- **Summary** – a concise summary of the content
- **Action Items** – tasks and actions mentioned in the video
- **Key Decisions** – important decisions and conclusions
- **Open Questions** – questions or topics that remain unresolved

---

## 🧠 Retrieval-Augmented Generation

The application uses a RAG pipeline that lets users ask questions about the processed video.

```text
Transcript → Text Splitting → Transcript Chunks → HuggingFace Embeddings
→ ChromaDB → Similarity Search → Relevant Context → Groq LLM → Generated Answer
```

Instead of sending the entire transcript for every question, the system retrieves only the relevant transcript sections and uses them as context for the LLM.

### Example Questions

- What are the main topics discussed?
- What decisions were made?
- What are the action items?
- What questions remain unanswered?
- What are the main conclusions?
- Summarize the discussion about the project.
- Explain the main concept discussed in the video.

---

## 🧩 Project Components

| File | Responsibility |
|------|----------------|
| `app.py` | Streamlit frontend: user input, file uploading, processing controls, displaying summaries/insights/transcript, interactive video Q&A |
| `main.py` | Main pipeline: input → audio processing → transcription → title → summarization → information extraction → RAG creation |
| `core/transcriber.py` | Speech-to-text with OpenAI Whisper: processing audio chunks, running Whisper, generating transcript text |
| `core/summarize.py` | LLM-based title and summary generation |
| `core/extractor.py` | Extracts action items, key decisions, and open questions |
| `core/rag_engine.py` | RAG system: text splitting, embedding generation, vector database creation, document retrieval, question answering |
| `utils/audio_processor.py` | Input handling: detecting input type, processing YouTube URLs, downloading audio, audio conversion, preparing audio for transcription |

---

## 📦 Requirements

The project uses the following major Python packages:

```text
streamlit
yt-dlp
ffmpeg-python
audioop-lts
pydub

openai-whisper
torch
numpy

langchain
langchain-core
langchain-community
langchain-text-splitters
langchain-groq

chromadb
langchain-chroma
langchain-huggingface
sentence-transformers

sarvamai
transformers
accelerate

fpdf2
python-dotenv
```

The complete dependency configuration is available in `requirements.txt`.

---

## 🎯 Use Cases

**🎓 Education** – Summarize lectures, extract important concepts, search through educational videos, and ask questions about course material.

**💼 Meetings** – Generate summaries, extract action items, identify decisions, find unresolved questions, and ask questions about the meeting.

**📺 YouTube Content** – Understand main topics, generate summaries, extract important information, and search through long-form videos.

**🧑‍💻 Technical Videos** – Extract key concepts, summarize tutorials, ask questions about implementations, and search transcripts semantically.

---

## 🌐 Language Support

The application is designed to support:

- English
- Hinglish
- Hindi-related processing workflows

Sarvam AI can be used for Hindi-to-English language processing where required.

---

## ⚠️ Important Notes

- **FFmpeg** must be installed separately from the Python packages.
- **Whisper** runs locally and therefore requires sufficient system resources for transcription.
- **YouTube** extraction depends on `yt-dlp` and YouTube's current media delivery and extraction requirements.
- **Vector Database** – the Chroma database is generated locally and does not need to be committed.
- **Downloaded Files** – audio files are runtime-generated and should not be committed to GitHub.
- **API Keys** – never hard-code them in Python files; always load them from environment variables.

---

## 🧪 Example Workflow

1. Open the Streamlit application
2. Enter a YouTube URL or upload a local file
3. Start processing
4. Audio is extracted and prepared
5. Whisper generates the transcript
6. AI generates the title and summary
7. Action items, decisions, and questions are extracted
8. The transcript is converted into embeddings
9. Embeddings are stored in ChromaDB
10. Ask questions about the video
11. RAG retrieves relevant transcript context
12. Groq LLM generates the answer

---

## 🚀 Future Improvements

- 🎬 Timestamp-based transcript navigation
- 📌 Video chapter generation
- 🔍 Improved transcript search
- 📄 Automated PDF report generation
- 🌍 Expanded multilingual support
- ⚡ Faster processing pipeline
- 💾 Persistent conversation history
- 🎯 More advanced agentic video analysis
- ☁️ Cloud deployment
- 📊 Topic and content analytics

---

## ⭐ Project Objective

The objective of this project is to build an end-to-end Generative AI application that transforms long-form video content into an interactive knowledge assistant.

```text
Video / Audio → Speech-to-Text → Transcript Understanding
→ Structured Information Extraction → Embeddings → Vector Database
→ Retrieval-Augmented Generation → Interactive AI Assistant
```

This demonstrates practical use of:

- LLM integration
- Prompt-based information extraction
- Embeddings and vector databases
- Semantic retrieval
- Retrieval-Augmented Generation
- Local speech-to-text
- LangChain
- Streamlit

---

## 👨‍💻 Author

**Abdul Ahad Shaikh**
BCA Graduate | Aspiring Data Analyst | GenAI & Machine Learning Enthusiast

**Areas of Interest:** Generative AI · Agentic AI · Large Language Models · Retrieval-Augmented Generation · Machine Learning · Data Analytics · Python · SQL · Power BI

---

## 📄 License

This project is intended for educational, learning, and portfolio purposes.