# Robo-Blogger: AI-Powered Blog Generation with LangGraph

An intelligent blog writing system that uses LangGraph to orchestrate complex AI workflows for generating high-quality, research-backed blog posts.

## 🚀 Overview

Robo-Blogger is a sophisticated AI-powered content generation system that:

- **Plans blog structure** using AI to break down content into logical sections
- **Researches topics** by scraping provided URLs for additional context
- **Writes sections in parallel** using LangGraph's concurrent processing capabilities
- **Compiles final content** into a complete, well-structured blog post
- **Uses WRITER AI** as the underlying language model for content generation

### Key Features

- **Intelligent Planning**: AI analyzes notes and creates structured blog outlines
- **Web Research**: Automatically scrapes and incorporates information from provided URLs
- **Parallel Processing**: Multiple sections written simultaneously for efficiency
- **Structured Output**: Uses WRITER's native structured output for reliable, validated content generation
- **Configurable**: Customizable blog structure and requirements

## 📋 Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- WRITER API key (required)
- LangSmith API key (optional - for dashboard observability)

## 🔧 Installation & Setup

### 1. Clone and Navigate to Project
```bash
git clone <your-repo-url>
cd LangChain-examples
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Set Up Environment Variables

#### Required: WRITER API Key
```bash
# Option A: Environment variable
export WRITER_API_KEY="your_WRITER_api_key_here"

# Option B: .env file (recommended)
cp .env.template .env
# Edit .env file with your WRITER API key
```

#### Optional: LangSmith API Key (for dashboard)
```bash
# Add to your .env file for dashboard observability:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=robo-blogger
```

## 🚀 Quick Start

### 1. Prepare Your Blog Content
Edit `src/notes/workflows.txt` with your blog topic:
```bash
# Example content for workflows.txt
I want to write a blog post about WRITER workflows

We get this question all the time at WRITER AI Framework

A workflow is a sequence of connected blocks, where each block performs a specific action. 
Think of it like a chain reaction - when one block completes its task, it triggers the next block in line.

WRITER Workflows is currently in beta, which means we're still actively improving features and adding functionality.

Workflows save time and effort by automating repetitive tasks.
```

### 2. Add Research URLs (Optional)
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

### 3. Run the Blog Generator
```bash
poetry run python src/main.py
```

### 4. Find Your Generated Blog
The blog will be saved to `src/results/` with a timestamp:
```
src/results/blog_20241201_143022.md
```

## 🎯 How It Works

### Workflow Overview

1. **Blog Planning Phase**
   - Reads user notes from `src/notes/workflows.txt`
   - Uses AI to create structured blog outline
   - Defines sections (introduction, main body, conclusion)

2. **Research Phase**
   - Scrapes content from provided URLs
   - Extracts relevant information for each section

3. **Parallel Writing Phase**
   - Writes main body sections concurrently
   - Each section uses research data and user notes

4. **Final Assembly Phase**
   - Writes introduction and conclusion using completed sections as context
   - Compiles all sections into final blog post


## 📊 LangGraph Dashboard (LangSmith)

### Enable Dashboard Observability

To see your workflow in the LangGraph dashboard:

1. **Get a LangSmith API Key**:
   - Visit [LangSmith](https://smith.langchain.com/)
   - Sign up/log in to your account
   - Go to API Keys section
   - Generate a new API key

2. **Add to your `.env` file**:
   ```
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_langsmith_api_key_here
   LANGCHAIN_PROJECT=robo-blogger
   ```

3. **Run Your Workflow**:
   ```bash
   poetry run python src/main.py
   ```

4. **View in Dashboard**:
   - Go to [LangSmith Dashboard](https://smith.langchain.com/)
   - Navigate to the "robo-blogger" project
   - See your workflow execution with step-by-step flow, timing, and error tracking

## 📚 Advanced Usage

### Custom Prompts
Edit `src/prompts.py` to customize AI prompts for blog planning and section writing.

### State Management
The system uses LangGraph's state management for passing data between workflow steps and managing parallel section writing.

### Adding New Features
- **New Section Types**: Modify `state.py`
- **Custom Research**: Extend `utils.py` for additional data sources
- **Different Output Formats**: Modify the final compilation step in `graph.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangGraph**: For workflow orchestration capabilities
- **WRITER AI**: For the underlying language model
- **LangChain**: For the AI framework integration

---

**Happy Blogging! 🚀**