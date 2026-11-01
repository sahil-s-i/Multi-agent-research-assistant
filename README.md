# Multi-Agent Research Assistant

A Gradio-based research assistant that coordinates specialized AI agents to clarify a user's query, plan research, search the web, and generate a structured report.

## Features

- **Query clarification:** Asks follow-up questions when a request needs more context.
- **Research planning:** Creates a structured plan with a search query.
- **Web search:** Retrieves results and source links using DuckDuckGo Search.
- **Report writing:** Produces a Markdown research report from the search results.
- **Interactive interface:** Uses Gradio to display the conversation and workflow status.
- **Email draft output:** Creates an email-formatted version of the report and appends it to `send_email.txt`.

> The current email tool saves content to a local text file; it does not deliver email.

## Workflow

1. Enter a research query in the Gradio interface.
2. The Manager Agent decides whether clarification is needed.
3. The Planner Agent creates a search plan.
4. The Search Agent retrieves web results.
5. The Writer Agent produces a structured report.
6. If the workflow invokes the Email Agent, it writes the email content to `send_email.txt`.

## Project structure

- `app.py` — Gradio interface and session workflow.
- `manager.py` — Manager Agent, response schema, and agent orchestration.
- `model.py` — Gemini model configuration and API client setup.
- `prompt_agent.py` — Query clarification agent.
- `planner_agent.py` — Structured research planning agent.
- `search_agent.py` — DuckDuckGo search tool and search agent.
- `writer_agent.py` — Research report writing agent and output schema.
- `email_agent.py` — Email composition instructions and local file output tool.

## Requirements

The project uses Python packages including:

- `gradio`
- `python-dotenv`
- `openai`
- `pydantic`
- `ddgs`
- `openai-agents` (the package that provides the `agents` module)

Install the dependencies in your Python environment. For example:

```bash
pip install gradio python-dotenv openai pydantic ddgs openai-agents
```

## Configuration

Create a `.env` file in the project directory and add your Google AI API key:

```env
GOOGLE_API_KEY=your_google_api_key
```

The model configuration also declares OpenRouter settings, but the current agent configuration uses the Gemini model. 

## Run

From the project directory, run:

```bash
python app.py
```

Open the local Gradio URL shown in the terminal.

## Notes

- The planner is currently configured to produce one search query.
- Search results depend on the DuckDuckGo Search service and may vary.
- The email tool writes a draft to `send_email.txt`; it is not connected to an email provider.
- The project requires valid API credentials and network access to use the configured model and web search.

