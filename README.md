# 🎓 Student Assistant MCP Server

A comprehensive [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built with Python and FastMCP. Designed to assist students with weighted grade calculations, secure study note management, dynamic class schedule lookups, research summarization with LLM sampling, and exam prep workflows.

---

## 🚀 Features

### 🛠️ Tools
* **`calculate_grade(homework, midterm, final_exam)`**: Computes weighted final grade (30% Homework, 30% Midterm, 40% Final Exam) and assigns letter grades (A, B, C, D, F).
* **`save_study_note(filename, content)`**: Saves notes into the sandboxed `./study_files/` directory with path traversal protection.
* **`smart_summarize(topic, num_pages)`**: Simulates multi-page research fetching with real-time progress reporting and Host LLM sampling.

### 📚 Resources
* **`student://schedule`**: Reads the student's weekly course schedule.
* **`notes://read/{filename}`**: Dynamically reads saved notes from the sandboxed study files directory.

### 📝 Prompts
* **`exam_prep(subject, difficulty)`**: Generates a structured 3-day study plan, key topics, and sample practice questions.

---

## 📦 Installation & Prerequisites

### 1. Clone the Repository
```bash
git clone https://github.com/kevinraj23/student-assistant-mcp-server.git
cd student-assistant-mcp-server
```

### 2. Install Dependencies
Ensure Python 3.10+ is installed:

Using `pip`:
```bash
pip install -r requirements.txt
```

Or using `uv`:
```bash
uv pip install -r requirements.txt
```

> **Note**: This server uses `mcp<2` (`mcp==1.30.0`) for compatibility with FastMCP v1 conventions.

---

## 🏃 Usage

### 1. Interactive Testing with MCP Inspector
Run the visual MCP Inspector web interface:
```bash
mcp dev student_assistant_server.py
```
Open your browser to the URL provided (default: `http://127.0.0.1:6274`) to test all tools, resources, and prompts interactively.

### 2. Running in Stdio Mode (MCP Clients / Claude Desktop)
To run directly via stdio:
```bash
python student_assistant_server.py
```

### 3. Claude Desktop Configuration
To connect this server to Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "student-assistant": {
      "command": "python",
      "args": [
        "c:/Users/aravindhan/Desktop/crowd-source-faq/student-assistant-mcp-server/student_assistant_server.py"
      ]
    }
  }
}
```

Or install it automatically with:
```bash
mcp install student_assistant_server.py
```

---

## 🛡️ Security
* **Path Traversal Defense**: All file read/write operations validate target paths to ensure files stay strictly within `./study_files/`.

---

## 📄 License
MIT License
