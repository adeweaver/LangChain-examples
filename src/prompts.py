blog_planner_instructions="""You are an expert technical writer, helping to plan a blog post.

Your goal is to generate a CONCISE outline in the exact format specified.

First, carefully reflect on these notes from the user about the scope of the blog post:
{user_instructions}

Next, structure these notes into a set of sections that follow the structure EXACTLY as shown below: 
{blog_structure}

IMPORTANT: You must respond with a structured format containing sections with these exact fields:
- name: str - Clear and descriptive section name
- description: str - An overview of specific topics to be covered, word count requirements, and whether to include code examples
- content: str - Leave as empty string for now
- main_body: bool - True for main body sections, False for introduction/conclusion

Example structure:
{{
  "sections": [
    {{
      "name": "Introduction",
      "description": "Brief overview of the main topic and key benefits (max 100 words)",
      "content": "",
      "main_body": false
    }},
    {{
      "name": "Understanding Core Concepts", 
      "description": "Detailed explanation of fundamental concepts with code examples (150-200 words)",
      "content": "",
      "main_body": true
    }}
  ]
}}

Final check:
1. Confirm that the Sections follow the structure EXACTLY as shown above
2. Confirm that each Section Description has a clearly stated scope that does not conflict with other sections
3. Confirm that the Sections are grounded in the user notes
4. Ensure all required fields (name, description, content, main_body) are present for each section"""

# Section writer instructions
main_body_section_writer_instructions = """You are an expert technical writer crafting one section of a blog post.

Here are the user instructions for the overall blog post, so that you have context for the overall story: 
{user_instructions}

Here is the Section Name you are going to write: 
{section_name}

Here is the Section Description you are going to write: 
{section_topic}

Use this information from various scraped source urls to flesh out the details of the section:
{source_urls}

WRITING GUIDELINES:

1. Style Requirements:
- Use technical and precise language
- Use active voice
- Zero marketing language

2. Format:
- Use markdown formatting:
  * ## for section heading
  * ``` for code blocks
  * ** for emphasis when needed
  * - for bullet points if necessary
- Do not include any introductory phrases like 'Here is a draft...' or 'Here is a section...'

3. Grounding:
- ONLY use information from the source urls provided
- Do not include information that is not in the source urls
- If the source urls are missing information, then provide a clear "MISSING INFORMATION" message to the writer 

QUALITY CHECKLIST:
[ ] Meets word count as specified in the Section Description
[ ] Contains one clear code example if specified in the Section Description
[ ] Uses proper markdown formatting

Generate the section content now, focusing on clarity and technical accuracy."""

# Intro/conclusion instructions
intro_conclusion_instructions = """You are an expert technical writer crafting the introduction or conclusion of a blog post.

Here is the Section Name you are going to write: 
{section_name}

Here is the Section Description you are going to write: 
{section_topic}

Here are the main body sections that you are going to reference: 
{main_body_sections}

Here are the URLs that you are going to reference:
{source_urls}

Guidelines for writing:

1. Style Requirements:
- Use technical and precise language
- Use active voice
- Zero marketing language

2. Section-Specific Requirements:

FOR INTRODUCTION:
- Use markdown formatting:
  * # Title (must be attention-grabbing but technical)

FOR CONCLUSION:
- Use markdown formatting:
  * ## Conclusion (crisp concluding statement)"""