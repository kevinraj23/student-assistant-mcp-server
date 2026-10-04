# student_assistant_server.py
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

# ==============================================================================
# Day 1: Create the MCP Server (The "Server" role)
# ==============================================================================
mcp = FastMCP("StudentAssistant")

# ==============================================================================
# Day 9: Security – Define a safe sandbox root
# ==============================================================================
ALLOWED_ROOT = Path("./study_files").resolve()
ALLOWED_ROOT.mkdir(exist_ok=True)


# ==============================================================================
# Day 3: TOOLS – Actions the AI can execute
# ==============================================================================

@mcp.tool()
def calculate_grade(homework: float, midterm: float, final_exam: float) -> str:
    """Calculate a student's weighted final grade.
    Weights: Homework 30%, Midterm 30%, Final Exam 40%."""
    if any(g < 0 or g > 100 for g in [homework, midterm, final_exam]):
        return "Error: All grades must be between 0 and 100."

    weighted = (homework * 0.30) + (midterm * 0.30) + (final_exam * 0.40)
    letter = (
        "A" if weighted >= 90 else
        "B" if weighted >= 80 else
        "C" if weighted >= 70 else
        "D" if weighted >= 60 else "F"
    )
    return f"Final Grade: {weighted:.1f}% ({letter})"


@mcp.tool()
def save_study_note(filename: str, content: str) -> str:
    """Save a study note to the allowed study_files directory."""
    # Day 9: Path traversal defense!
    target = (ALLOWED_ROOT / filename).resolve()
    if not target.is_relative_to(ALLOWED_ROOT):
        return "SECURITY ALERT: Access denied - path traversal detected!"

    target.write_text(content, encoding="utf-8")
    return f"Note saved to {filename} successfully."


# Day 8 & 10: A long-running tool with Progress + Sampling
@mcp.tool()
async def smart_summarize(topic: str, num_pages: int, ctx: Context) -> str:
    """Simulate fetching research pages and use the Host's AI to summarize them."""

    collected_text = ""
    for i in range(1, num_pages + 1):
        await asyncio.sleep(0.5)  # Simulating network fetch

        # Day 8: Report live progress to the user's UI
        await ctx.report_progress(progress=i, total=num_pages)
        await ctx.info(f"Fetched page {i} of {num_pages}...")

        collected_text += f"Page {i}: Key findings about {topic} from source {i}. "

    # Day 10: Use Sampling to borrow the Host's LLM brain!
    response = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Summarize this into 3 bullet points:\n{collected_text}"}
        ],
        max_tokens=150
    )

    return f"Research Summary for '{topic}':\n\n{response.text}"


# ==============================================================================
# Day 4: RESOURCES – Read-only contextual data via URIs
# ==============================================================================

@mcp.resource("student://schedule")
def get_class_schedule() -> str:
    """The student's current weekly class schedule."""
    return """
    WEEKLY SCHEDULE:
    Monday:    9 AM - Data Structures | 2 PM - Linear Algebra
    Tuesday:   10 AM - Operating Systems | 3 PM - Lab
    Wednesday: 9 AM - Data Structures | 1 PM - Discrete Math
    Thursday:  10 AM - Operating Systems | 3 PM - Lab
    Friday:    11 AM - Seminar | 2 PM - Office Hours
    """

# Day 4: Dynamic resource template with {variable}
@mcp.resource("notes://read/{filename}")
def read_study_note(filename: str) -> str:
    """Read a previously saved study note by filename."""
    # Day 9: Path security check
    target = (ALLOWED_ROOT / filename).resolve()
    if not target.is_relative_to(ALLOWED_ROOT):
        return "SECURITY ALERT: Access denied."
    if not target.exists():
        return f"No note found with name '{filename}'."
    return target.read_text(encoding="utf-8")


# ==============================================================================
# Day 5: PROMPTS – Reusable AI workflow templates
# ==============================================================================

@mcp.prompt()
def exam_prep(subject: str, difficulty: str = "intermediate") -> str:
    """Generate a structured exam preparation plan for any subject."""
    return f"""
    You are an expert academic tutor.
    Create a focused exam preparation plan for: {subject}
    Target difficulty level: {difficulty}

    Include:
    1. Top 5 topics to prioritize.
    2. One practice question for each topic.
    3. A recommended 3-day study schedule.
    """


# ==============================================================================
# Day 6: Run the server (Default: stdio transport)
# ==============================================================================
if __name__ == "__main__":
    # Day 6: Switch to mcp.run(transport="sse") for remote access!
    mcp.run(transport="stdio")
