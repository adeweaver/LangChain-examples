from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_community.chat_models.writer import ChatWriter
from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph

import configuration
from prompts import (
    blog_planner_instructions,
    main_body_section_writer_instructions,
    intro_conclusion_instructions
)
from state import (
    Sections,
    BlogState,
    BlogStateInput,
    BlogStateOutput,
    SectionState
)
from utils import (
    load_and_format_urls,
    read_dictation_file,
    format_sections
)


load_dotenv()

model = ChatWriter(model='palmyra-x5')

def generate_blog_plan(state: BlogState, config: RunnableConfig):
    """Generate the blog plan"""

    user_instructions = read_dictation_file(state.transcribed_notes_file)

    configurable = configuration.Configuration.from_runnable_config(config)
    blog_structure = configurable.blog_structure

    sections_prompt = blog_planner_instructions.format(user_instructions=user_instructions, blog_structure=blog_structure)

    # Use the ChatWriter model to generate the blog plan
    response = model.invoke([
        SystemMessage(content="You are a blog planning assistant. Generate a structured blog plan based on the user's requirements. Respond with a JSON object containing a 'sections' array where each section has 'name', 'description', and 'main_body' fields."),
        HumanMessage(content=sections_prompt)
    ])
    
    # Parse the response manually since structured output might not work with ChatWriter
    import json
    import re
    
    # Extract JSON from the response
    response_text = response.content if isinstance(response.content, str) else str(response.content)
    
    # Try to find JSON in the response - look for JSON block specifically
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if not json_match:
        # Fallback: try to find JSON without code block markers
        json_match = re.search(r'\{.*?"sections".*?\}', response_text, re.DOTALL)
    
    if json_match:
        try:
            json_data = json.loads(json_match.group(1) if json_match.groups() else json_match.group())
            report_sections = Sections(**json_data)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse JSON from response: {e}")
            print(f"Response content: {response_text}")
            raise ValueError("Failed to parse blog sections from response")
    else:
        print(f"No JSON found in response: {response_text}")
        raise ValueError("Failed to parse blog sections from response")
    
    if report_sections is None or not hasattr(report_sections, 'sections'):
        raise ValueError("Failed to parse blog sections from response")
    
    print("\n" + "="*80)
    print("📋 BLOG PLAN GENERATED")
    print("="*80)
    for i, section in enumerate(report_sections.sections, 1):
        print(f"\n{i}. {section.name}")
        print(f"   Description: {section.description}")
        print(f"   Main Body: {'✅' if section.main_body else '❌'}")
        print("-" * 60)
    print("="*80 + "\n")

    return {"sections": report_sections.sections, "user_instructions": user_instructions}

def write_section(state: SectionState):
    """Write a section of the blog"""

    section = state.section
    urls = state.urls
    user_instructions = state.user_instructions

    url_source_str = "" if not urls else load_and_format_urls(urls if isinstance(urls, list) else [urls])

    system_instructions = main_body_section_writer_instructions.format(section_name=section.name, 
                                                                       section_topic=section.description, 
                                                                       user_instructions=user_instructions, 
                                                                       source_urls=url_source_str)

    section_content = model.invoke([SystemMessage(content=system_instructions)] + [HumanMessage(content="Generate a blog section based on the provided information.")])
    
    section.content = section_content.content if isinstance(section_content.content, str) else str(section_content.content)
    
    print(f"✅ Completed: {section.name}")

    return {"completed_sections": [section]}

def write_final_sections(state: SectionState):
    """Write final sections of the blog"""

    section = state.section
    
    system_instructions = intro_conclusion_instructions.format(section_name=section.name, 
                                                               section_topic=section.description, 
                                                               main_body_sections=state.blog_main_body_sections, 
                                                               source_urls=state.urls)

    section_content = model.invoke([SystemMessage(content=system_instructions)] + [HumanMessage(content="Generate an intro/conclusion section based on the provided main body sections.")])
    
    section.content = section_content.content if isinstance(section_content.content, str) else str(section_content.content)
    
    print(f"✅ Completed: {section.name}")

    return {"completed_sections": [section]}

def initiate_section_writing(state: BlogState):
    """Kick off parallel writing of main body sections"""
        
    print(f"\n🚀 Starting parallel writing of {len([s for s in state.sections if s.main_body])} main body sections...")
    
    return [
        Send("write_section", SectionState(
            section=s,
            user_instructions=state.user_instructions,
            urls=state.urls,
            completed_sections=[]
        )) 
        for s in state.sections 
        if s.main_body
    ]

def gather_completed_sections(state: BlogState):
    """Gather completed main body sections"""

    completed_sections = state.completed_sections
    if completed_sections is None:
        completed_sections = []
    completed_report_sections = format_sections(completed_sections)
    
    print(f"\n📊 Gathered {len(completed_sections)} completed main body sections")

    return {"blog_main_body_sections": completed_report_sections}

def initiate_final_section_writing(state: BlogState):
    """Kick off parallel writing of final sections"""

    final_sections = [s for s in state.sections if not s.main_body]
    print(f"\n🚀 Starting parallel writing of {len(final_sections)} final sections...")
    
    return [
        Send("write_final_sections", SectionState(
            section=s,
            blog_main_body_sections=state.blog_main_body_sections,
            urls=state.urls,
            completed_sections=[]
        )) 
        for s in state.sections 
        if not s.main_body
    ]

def compile_final_blog(state: BlogState):
    """Compile the final blog"""

    sections = state.sections
    completed_sections = {s.name: s.content for s in state.completed_sections}

    for section in sections:
        section.content = completed_sections[section.name]

    all_sections = "\n\n".join([s.content for s in sections])
    
    print(f"\n🎉 Final blog compiled with {len(sections)} sections!")

    return {"final_blog": all_sections}

builder = StateGraph(BlogState, input=BlogStateInput, output=BlogStateOutput, config_schema=configuration.Configuration)
builder.add_node("generate_blog_plan", generate_blog_plan)
builder.add_node("write_section", write_section)
builder.add_node("compile_final_blog", compile_final_blog)
builder.add_node("gather_completed_sections", gather_completed_sections)
builder.add_node("write_final_sections", write_final_sections)
builder.add_edge(START, "generate_blog_plan")
builder.add_conditional_edges("generate_blog_plan", initiate_section_writing, ["write_section"])
builder.add_edge("write_section", "gather_completed_sections")
builder.add_conditional_edges("gather_completed_sections", initiate_final_section_writing, ["write_final_sections"])
builder.add_edge("write_final_sections", "compile_final_blog")
builder.add_edge("compile_final_blog", END)

graph = builder.compile() 
