# AI Video Assistant — Project Documentation

## 1. Introduction

AI Video Assistant turns a meeting recording or YouTube video into a transcript and a set of practical meeting notes. It uses speech recognition to convert audio into text, then uses a large language model to create a title, summary, action items, key decisions, and unresolved questions. Users can also ask questions about the transcript through a retrieval-augmented chat interface.

The application has a React web frontend and a Python API and processing backend. The frontend presents analysis results in a dark dashboard, allows users to chat with the transcript, and stores a local history of completed analyses in the browser.

## 2. Problem the Project Solves

Long recordings take time to review, and important details can be difficult to find later. In particular, teams may need to identify:

- What was discussed?
- What decisions were made?
- Who needs to do what, and by when?
- Which questions still need follow-up?
- What did the meeting say about a particular topic?

The project automates these tasks by transcribing recordings, extracting structured notes, and making the transcript searchable through natural-language questions. Its goal is to reduce manual note-taking and make meeting information easier to review and retrieve.

## 3. Use Cases

1. **Meeting recap:** Generate a concise summary after a team or project meeting.
2. **Action-item review:** Find tasks, owners, and deadlines mentioned in a recording.
3. **Decision tracking:** Collect important decisions in one place.
4. **Follow-up preparation:** Identify unresolved questions and topics needing clarification.
5. **Recorded lecture or interview review:** Summarize long-form speech and ask questions about its contents.
6. **YouTube content review:** Analyze the audio from a YouTube video without manually transcribing it.
7. **Transcript Q&A:** Ask a question in natural language and retrieve an answer grounded in the processed transcript.

## 4. Main Features

- Accepts a YouTube URL or a path to a local audio/video file.
- Downloads YouTube audio using `yt-dlp`.
- Converts input media to mono, 16 kHz WAV audio and splits it into 10-minute chunks.
- Transcribes chunks with a locally run Whisper model.
- Uses Gemini through LangChain to generate a meeting title, summary, action items, key decisions, and open questions.
- Builds a Chroma vector store over transcript chunks and uses Hugging Face sentence-transformer embeddings for retrieval.
- Answers transcript questions through a retrieval-augmented generation (RAG) chain.
- Renders Markdown formatting in generated results and AI responses.
- Provides a browser-based history page backed by `localStorage`.
- Provides a CLI entry point in addition to the HTTP API.

## 5. Technology Used

### Frontend

| Technology | Role |
|---|---|
| React 19 | User interface and reusable UI components |
| Vite | Frontend development server and production bundler |
| React Router | Client-side navigation |
| Tailwind CSS 4 | Utility-based styling and responsive dark UI |
| `react-markdown` and `remark-gfm` | Render Markdown, including lists, emphasis, and GitHub-flavored Markdown |
| `lucide-react` | Interface icons |

### Backend and AI

| Technology | Role |
|---|---|
| Python | Audio processing, transcription orchestration, and AI workflows |
| FastAPI | HTTP API and request validation |
| Uvicorn | ASGI server used to run the API |
| Pydantic | Request-body validation |
| `yt-dlp` | Download audio from YouTube URLs |
| `pydub` and FFmpeg | Convert, normalize, and split audio |
| OpenAI Whisper | Local speech-to-text transcription |
| LangChain | Prompt construction and model/retrieval chains |
| Google Gemini (`ChatGoogleGenerativeAI`) | Generate summaries, extracted notes, titles, and chat responses |
| Chroma | Store and search transcript embeddings |
| Hugging Face sentence-transformers | Create embeddings using `all-MiniLM-L6-v2` |
| `python-dotenv` | Load local environment variables from `.env` |

> **Dependency note:** The backend imports packages such as Whisper, LangChain community integrations, Chroma, Hugging Face embeddings, and text splitters. Check that the backend environment has all packages required by those imports; the current `backend/requirements.txt` may not enumerate every package used by the source.

## 6. Application Routes

### 6.1 Frontend routes

| Route | Page | Purpose |
|---|---|---|
| `/` | Home / analysis | Shows the welcome page before analysis, or the title, summary, transcript, extracted notes, and chat for the current analysis. |
| `/history` | Analysis history | Lists analyses saved in this browser. Selecting an entry opens it on the home page; entries can be deleted. |

The React application currently defines these two routes. It does not define a separate not-found route.

### 6.2 Backend API routes

The API is defined in `backend/server.py`. The frontend currently calls the backend at `http://localhost:8000`.

#### `GET /api/health`

Health check for the API.

**Response**

```json
{
  "status": "ok"
}
```

#### `POST /api/process`

Processes a YouTube URL or local media path. The operation may take a while because it downloads or converts media, runs transcription, and makes several model requests.

**Request**

```json
{
  "source": "https://www.youtube.com/watch?v=...",
  "language": "english"
}
```

`source` is required and must not be blank. `language` defaults to `"english"`.

**Successful response**

```json
{
  "session_id": "generated-session-id",
  "title": "Example Meeting",
  "summary": "Markdown-formatted summary...",
  "action_items": "Markdown-formatted action items...",
  "key_decisions": "Markdown-formatted decisions...",
  "open_questions": "Markdown-formatted follow-up questions...",
  "transcript": "Full transcript..."
}
```

The returned session ID is used for chat. A blank source produces HTTP `400`; a processing exception is returned as HTTP `500`.

#### `POST /api/chat`

Retrieves transcript passages relevant to the question and asks the language model to answer using those passages.

**Request**

```json
{
  "session_id": "generated-session-id",
  "question": "What decisions were made?"
}
```

**Successful response**

```json
{
  "answer": "Markdown-formatted answer..."
}
```

An unknown or expired in-memory session produces HTTP `404`. An error while running the chat chain produces HTTP `500`.

## 7. End-to-End Workflow

1. **Enter a source.** The user provides a YouTube URL or a path to a local media file in the sidebar and submits the analysis form.
2. **Send the processing request.** The frontend sends the source and selected language to `POST /api/process`.
3. **Resolve the media input.** The backend checks whether the source is an HTTP(S) URL. YouTube sources are downloaded as audio; other inputs are treated as local file paths.
4. **Normalize the audio.** The backend converts the audio to mono, 16 kHz WAV and divides it into 10-minute WAV chunks.
5. **Transcribe the chunks.** Whisper loads its configured model once per process and transcribes each audio chunk. The chunk texts are joined into one transcript.
6. **Generate meeting notes.** LangChain sends the transcript to Gemini workflows to produce a short title, a summary, action items, key decisions, and unresolved questions.
7. **Prepare transcript search.** The transcript is split into smaller passages, embedded with `all-MiniLM-L6-v2`, and added to a Chroma vector store. The RAG chain uses similarity retrieval (configured for four passages) to find context for chat questions.
8. **Create the chat session.** The backend generates a UUID and stores the RAG chain in an in-memory session map.
9. **Display and save the result.** The frontend displays the generated notes and transcript. It adds the analysis to browser `localStorage` history.
10. **Ask follow-up questions.** The frontend sends the current session ID and question to `POST /api/chat`. The backend retrieves relevant transcript passages and returns a concise answer; Markdown is rendered in the chat UI.

## 8. Project Structure

```text
backend/
  server.py                 FastAPI app and HTTP endpoints
  main.py                   Orchestrates the processing pipeline and CLI
  core/
    transcriber.py          Whisper model and chunk transcription
    Summarization.py        Meeting title and summary generation
    extractor.py            Action-item, decision, and question extraction
    vector_store.py         Transcript chunking, embeddings, and Chroma store
    rag_engine.py           Retrieval-augmented meeting chat
  utils/
    audio_preprocessing.py  YouTube download, audio conversion, and chunking
  requirements.txt          Backend Python package list
  Document/                 Existing setup and workflow notes

frontend/
  src/
    App.jsx                 Router and application provider
    context/AppContext.jsx  Current analysis and browser history state
    Components/             Layout, sidebar, input, results, Markdown, and chat
    pages/                  Home and history pages
  package.json              Frontend dependencies and scripts
```

## 9. Running the Project Locally

### Backend

1. Install Python dependencies into the backend's Python environment, including all packages imported by the backend source.
2. Install FFmpeg and ensure it is available on `PATH`; `pydub` relies on it for media conversion.
3. Configure the Google/Gemini API credential in the environment or a local `.env` file. Do not commit API keys.
4. From the `backend` directory, run the FastAPI app:

```powershell
uvicorn server:app --reload --port 8000
```

### Frontend

From the `frontend` directory:

```powershell
npm install
npm run dev
```

Open the Vite development URL (normally `http://localhost:5173`). The backend CORS configuration currently allows `localhost:5173` and `127.0.0.1:5173`.

## 10. Important Implementation Notes and Limitations

- **Language selection:** The frontend sends the selected language, but `run_pipeline` currently does not use its `language` argument to configure transcription. Whisper is called with its default transcription behavior.
- **Local file paths:** A local path is read by the backend machine. The browser does not upload a local file to the backend, so the path must be accessible to the backend process.
- **Session lifetime:** RAG chains are stored in process memory. Restarting the backend clears chat sessions; re-running analysis creates a new session.
- **History persistence:** Result history is stored in the browser's `localStorage`, not in a server-side database. The saved result can remain visible after a backend restart, but its old chat session may no longer exist.
- **Media storage:** Downloaded, converted, and chunked files are written to the backend's configured download folder. A cleanup/retention process is not implemented in the described flow.
- **Model configuration:** The transcription model defaults to Whisper `"small"` and can be overridden through `WHISPER_MODEL`. Chat and note generation use Gemini models configured in the Python source.
- **Grounding:** The chat prompt instructs the model to answer from the meeting transcript context and to state when the answer is not present. Retrieval-based responses can still depend on the retrieved passages and model output.

## 11. Summary

AI Video Assistant combines audio preprocessing, local speech recognition, generative meeting-note creation, and transcript-based conversational search. It is intended to make recordings easier to understand and revisit, while keeping the user workflow simple: provide a source, review the generated notes, and ask questions about the meeting.
