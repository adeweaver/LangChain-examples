# Article research & creation agent: AI-powered research, analysis, and content generation with LangGraph and WRITER

## 🚀 Overview

This Article research & creation agent is a sophisticated AI-powered 
agent that transforms dictation into polished articles. Inspired by 
[Lance's robo-blogger project](https://github.com/langchain-ai/
robo-blogger), it combines **LangGraph** for workflow orchestration 
with **WRITER** for intelligent research, analysis, and content 
generation:

### Key Features

- **Dictation to article**: Transforms voice dictation into polished articles
- **Web research**: Scrapes and incorporates information from provided URLs
- **Intelligent planning**: WRITER analyzes dictation notes and creates structured article outlines using native structured output
structured article outlines using native structured output
- **Parallel processing**: Multiple sections written simultaneously 
using LangGraph with WRITER's Palmyra X5 model
- **Structured output**: Uses WRITER's native structured output 
capabilities for consistent, well-formatted content

## 📋 Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- WRITER API key (required)
- LangSmith API key (optional - for dashboard observability)

## 🔧 Installation & Setup

### 1. Clone and navigate to project
```bash
git clone https://github.com/adeweaver/LangChain-examples.git
cd LangChain-examples
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Set up environment variables

#### Required: WRITER API key
```bash
# Option A: Environment variable
export WRITER_API_KEY="your_WRITER_API_key_here"

# Option B: .env file (recommended)
cp .env.template .env
# Edit .env file with your WRITER API key
```

#### Optional: LangSmith API key (for dashboard)
```bash
# Add to your .env file for dashboard observability:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=blog-generator
```

## 🚀 Quick Start

### 1. Prepare your dictation notes
Edit `src/notes/workflows.txt` with your dictation content:
```bash
# Example content for workflows.txt (your voice dictation)
I want to write an article about AI-powered content creation

We get this question all the time at our company

The key insight is that our best ideas often come when we're away from the keyboard - while walking, commuting, or right after a meeting.

AI can help transform these raw thoughts into polished content while maintaining the authenticity of your original ideas.

The workflow separates idea capture from content structuring, helping maintain the natural flow of thoughts while ensuring professional presentation.
```

### 2. Add research URLs (optional)
Edit `src/main.py` to add URLs for additional research context:
```python
input_data = BlogStateInput(
    transcribed_notes_file="workflows.txt",
    urls=[
        "https://dev.writer.com/home/introduction",
        "https://dev.writer.com/no-code/introduction"
        # Add your own research URLs here
    ])
```

### 3. Run the article research & creation agent
```bash
poetry run python src/main.py
```

### 4. Find your generated article
The article will be saved to `src/results/` with a timestamp:
```
src/results/blog_20241201_143022.md
```

## 🎯 How It Works

![Workflow Diagram](assets/flow_diagram.png)

### Workflow overview

1. **Article planning phase**
   - Reads dictation notes from `src/notes/workflows.txt`
   - Uses AI to create structured article outline
   - Defines sections (introduction, main body, conclusion)

2. **Research phase**
   - Scrapes content from provided URLs
   - Extracts relevant information for each section

3. **Parallel writing phase**
   - Writes main body sections concurrently
   - Each section uses research data and dictation notes

4. **Final assembly phase**
   - Writes introduction and conclusion using completed sections as context
   - Compiles all sections into final article

**Happy writing! 🚀**