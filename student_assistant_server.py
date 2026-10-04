import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("StudentAssistant")

# Sandbox folder for saving and reading student notes
ALLOWED_ROOT = Path("./study_files").resolve()
ALLOWED_ROOT.mkdir(exist_ok=True)


# --- Tools ---

@mcp.tool()
def calculate_grade(homework: float, midterm: float, final_exam: float) -> str:
    """Calculate weighted final grade (30% HW, 30% Midterm, 40% Final Exam)."""
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
    target = (ALLOWED_ROOT / filename).resolve()
    if not target.is_relative_to(ALLOWED_ROOT):
        return "Security Alert: Access denied - path traversal detected."

    target.write_text(content, encoding="utf-8")
    return f"Note saved to {filename} successfully."


@mcp.tool()
async def smart_summarize(topic: str, num_pages: int, ctx: Context) -> str:
    """Fetch research pages and summarize content using host sampling."""
    collected_text = ""
    for i in range(1, num_pages + 1):
        await asyncio.sleep(0.5)

        await ctx.report_progress(progress=i, total=num_pages)
        await ctx.info(f"Fetched page {i} of {num_pages}...")

        collected_text += f"Page {i}: Key findings about {topic} from source {i}. "

    response = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Summarize this into 3 bullet points:\n{collected_text}"}
        ],
        max_tokens=150
    )

    return f"Research Summary for '{topic}':\n\n{response.text}"


# --- Resources ---

@mcp.resource("student://schedule")
def get_class_schedule() -> str:
    """The student's current weekly class schedule."""
    return """WEEKLY SCHEDULE:
Monday:    9 AM - Data Structures | 2 PM - Linear Algebra
Tuesday:   10 AM - Operating Systems | 3 PM - Lab
Wednesday: 9 AM - Data Structures | 1 PM - Discrete Math
Thursday:  10 AM - Operating Systems | 3 PM - Lab
Friday:    11 AM - Seminar | 2 PM - Office Hours
"""


@mcp.resource("notes://read/{filename}")
def read_study_note(filename: str) -> str:
    """Read a saved study note by filename."""
    target = (ALLOWED_ROOT / filename).resolve()
    if not target.is_relative_to(ALLOWED_ROOT):
        return "Security Alert: Access denied."
    if not target.exists():
        return f"No note found with name '{filename}'."
    return target.read_text(encoding="utf-8")


# --- Prompts ---

@mcp.prompt()
def exam_prep(subject: str, difficulty: str = "intermediate") -> str:
    """Generate a structured exam preparation plan."""
    return f"""You are an expert academic tutor.
Create a focused exam preparation plan for: {subject}
Target difficulty level: {difficulty}

Include:
1. Top 5 topics to prioritize.
2. One practice question for each topic.
3. A recommended 3-day study schedule.
"""


if __name__ == "__main__":
    mcp.run(transport="stdio")
