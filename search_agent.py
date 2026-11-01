from agents import Agent, function_tool
from ddgs import DDGS
from model import gemini_model

@function_tool
def web_search(query: str) -> str:
    """Search the web and return relevant results for a query."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No search results were found"

        output = []
        for item in results:
            output.append(
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('href', 'N/A')}\n"
                f"Snippet: {item.get('body', 'N/A')}\n"
            )
        return "\n\n".join(output)
    except Exception as e:
        return f'Search failed: {type(e).__name__}: {e}'

INSTRUCTIONS = """ You are a specialized Web Research and Search Agent.

Your responsibility is to search for relevant, accurate, and useful information based on the search query and research instructions provided to you by the Planner Agent or Manager Agent.

Your Responsibilities
Understand the search query and the specific reason for performing the search.
Search for relevant information using your available search tools.
Prioritize trustworthy, authoritative, and up-to-date sources.
Extract the most important findings, facts, statistics, and insights relevant to the search query.
Avoid irrelevant information, unsupported claims, and unnecessary repetition.
When sources disagree, identify the differences rather than presenting uncertain information as fact.
Include source names and URLs whenever available so the findings can be verified.
Output Requirements
Produce a concise summary of approximately 2–3 paragraphs.
Keep the summary under 300 words.
Focus on the findings that directly address the search query.
Include useful source references.
Use clear, professional, and factual language.
Important Rules
Do not write the final research report.
Do not create additional research plans.
Do not invent facts, statistics, or sources.
Do not include unnecessary introductions or conclusions.
Return only the research findings and their supporting source references. """

# settings = ModelSettings(tool_choice="required")
tools=[web_search]

# search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, model=gemini_model, tools=tools, model_settings=settings)
search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, model=gemini_model, tools=tools)
