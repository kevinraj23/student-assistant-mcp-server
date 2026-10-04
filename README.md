# Student Assistant MCP Server

A simple Model Context Protocol (MCP) server for handling common student tasks, including weighted grade calculations, study note management, class schedule lookups, and study plan prompts.

## Features

### Tools
- `calculate_grade(homework, midterm, final_exam)`: Computes weighted course averages (30% HW, 30% Midterm, 40% Final) and outputs letter grades.
- `save_study_note(filename, content)`: Writes text notes into `./study_files/` with path validation.
- `smart_summarize(topic, num_pages)`: Simulates paginated research fetching with progress reporting and LLM sampling.

### Resources
- `student://schedule`: Static URI returning the student's weekly schedule.
- `notes://read/{filename}`: Dynamic resource reading saved note files from the local directory.

### Prompts
- `exam_prep(subject, difficulty)`: Structured prompt template generating a 3-day study plan with key topics and review questions.

## Requirements

- Python 3.10+
- `mcp<2` (FastMCP v1)

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/kevinraj23/student-assistant-mcp-server.git
cd student-assistant-mcp-server
pip install -r requirements.txt
```

## Running

### Testing with MCP Inspector
To inspect and test tools interactively:

```bash
mcp dev student_assistant_server.py
```

### Running via Stdio
To run standard I/O mode for MCP client connections:

```bash
python student_assistant_server.py
```

### Claude Desktop Configuration
Add the server entry to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "student-assistant": {
      "command": "python",
      "args": [
        "C:/path/to/student-assistant-mcp-server/student_assistant_server.py"
      ]
    }
  }
}
```

Or install automatically:

```bash
mcp install student_assistant_server.py
```

## License

MIT
