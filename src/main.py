from graph import graph
from state import BlogStateInput
from datetime import datetime
import os

input_data = BlogStateInput(
    transcribed_notes_file="workflows.txt",
    urls=[
        "https://dev.writer.com/home/introduction",
        "https://dev.writer.com/no-code/introduction"
    ])

print("🚀 Starting Blog Generator...")
print(f"📝 Reading notes from: notes/workflows.txt")

response = graph.invoke(input=input_data)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"results/blog_{timestamp}.md"

os.makedirs("results", exist_ok=True)

with open(output_filename, "w") as f:
    f.write(response["final_blog"])

print(f"✅ Blog generated successfully!")
print(f"📄 Output saved to: {output_filename}")
print(f"📊 Check the LangSmith dashboard for execution details!")
