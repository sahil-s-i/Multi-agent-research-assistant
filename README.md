# Multi-Agent Research Assistant

A Gradio-based research assistant that coordinates specialized AI agents to clarify a research query, plan web searches, gather information, and generate a structured report.

## Features

- Clarifies ambiguous research requests through a Prompt Agent.
- Creates a structured plan containing five distinct search queries.
- Searches the web with DuckDuckGo Search and returns source titles, URLs, and snippets.
- Generates a Markdown research report with a Writer Agent.
- Displays workflow status in a Gradio chat interface.
- Sends a report by email through SMTP when configured; otherwise saves an email draft to `send_email.txt`.
- Supports Gemini as the configured model and includes an OpenRouter model configuration that can be selected as a fallback by changing the model used by the agents.

## Agent workflow

1. The Manager Agent determines whether the request needs clarification.
2. The Prompt Agent helps clarify the request when needed.
3. The Planner Agent prepares five search queries.
4. The Search Agent retrieves results for the planned queries.
5. The Writer Agent creates a structured report.
6. The Email Agent sends the report only when requested and a recipient is provided. Without SMTP configuration, it saves a draft instead.

## Project files

- `app.py` — Gradio UI, session state, and streamed workflow status.
- `manager.py` — Manager Agent, workflow orchestration, and response schema.
- `model.py` — Gemini and OpenRouter model/client configuration.
- `prompt_agent.py` — Query clarification instructions.
- `planner_agent.py` — Search plan schema and five-query planning instructions.
- `search_agent.py` — DuckDuckGo search tool and Search Agent.
- `writer_agent.py` — Report instructions and structured output schema.
- `email_agent.py` — SMTP email delivery with local draft fallback.

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project directory. Keep it out of version control and never commit API keys or SMTP credentials.

For Gemini:

```env
GOOGLE_API_KEY=your_google_api_key
```

For the OpenRouter model configured in `model.py`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

To enable actual email delivery, configure SMTP:

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
EMAIL_FROM=you@example.com
```

Use port `465` for implicit SSL. Other configured ports use STARTTLS. Email is sent only when a recipient is supplied and SMTP host and sender are configured. If SMTP is not configured, the tool saves the message to `send_email.txt` and reports that no delivery occurred.

`model.py` currently constructs both Gemini and OpenRouter clients, but the agents import `gemini_model`. To switch models when Gemini is unavailable, update the agents' model selection to use `openrouter_model` (or implement explicit fallback selection); merely configuring the OpenRouter client does not automatically fail over.

## Run

```bash
python app.py
```

Open the local Gradio URL printed in the terminal.

## Current limitations

- The planner is set to produce five search queries, but verify that the Manager Agent executes every planned query before describing the system as consistently performing five searches per request.
- Search results depend on the external DuckDuckGo Search service and the configured language model.
- SMTP delivery depends on valid server settings, credentials, network access, and a valid recipient.
