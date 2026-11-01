
import gradio as gr
from dotenv import load_dotenv
from agents import Runner
from manager import manager_agent

load_dotenv(override=True)

def create_session():
    return {
        "active_query": None,
        "active_messages": [],
        "awaiting_clarification": False,
        "research_history": []
    }

STATUS_MESSAGES = {
    "Prompt tool": {
        "start": "🔎 Understanding your requirements...",
        "done": "✅ Requirements understood."
    },
    "Planner tool": {
        "start": "📋 Creating your research plan...",
        "done": "✅ Research plan completed."
    },
    "Search tool": {
        "start": "🌐 Searching for relevant information...",
        "done": "✅ Search results collected."
    },
    "Writer tool": {
        "start": "📝 Writing your research report...",
        "done": "✅ Research report generated."
    },
    "Email tool": {
        "start": "📧 Preparing and sending your email...",
        "done": "✅ Email delivery completed."
    }
}

def get_status(tool_name, stage="start"):
    status = STATUS_MESSAGES.get(tool_name)

    if status:
        return status.get(stage, "Manager Agent is processing...")

    return "⚙️ Manager Agent is coordinating the workflow..."

def format_conversation(messages):
    return "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in messages
    )

async def run_manager(message, history, session):

    if not message.strip():
        yield history, session, "Please enter a query.", ""
        return

    if session is None:
        session = create_session()

    # Start a fresh research context unless
    # we are answering a clarification question.
    if not session["awaiting_clarification"]:
        session["active_query"] = message
        session["active_messages"] = []

    # Save user message
    session["active_messages"].append({
        "role": "user",
        "content": message
    })

    history = history or []
    history.append({
        "role": "user",
        "content": message
    })

    conversation = format_conversation(
        session["active_messages"]
    )

    yield (
        history,
        session,
        "Manager Agent is analyzing your request...",
        ""
    )

    result = Runner.run_streamed(
        manager_agent,
        input=(
            f"Original query: {session['active_query']}\n\n"
            f"Conversation:\n{conversation}"
        )
    )

    async for event in result.stream_events():

        if event.type == "run_item_stream_event":

            item = event.item
            raw_item = getattr(item, "raw_item", None)

            tool_name = getattr(raw_item, "name", "")

            if event.name == "tool_called":
                status = get_status(tool_name, "start")

            elif event.name == "tool_output":
                status = get_status(tool_name, "done")

            else:
                continue

            yield history, session, status, ""

    # ---------------------------------
    # GET FINAL MANAGER RESPONSE
    # ---------------------------------

    response = result.final_output

    if response.status == "clarification_needed":
        session["awaiting_clarification"] = True

        history.append({
            "role": "assistant",
            "content": response.message
        })

        session["active_messages"].append({
            "role": "assistant",
            "content": response.message
        })

        yield (
            history,
            session,
            "Waiting for your clarification.",
            ""
        )

        return

    # ---------------------------------
    # RESEARCH COMPLETED
    # ---------------------------------

    session["awaiting_clarification"] = False

    final_report = response.report or response.message

    history.append({
        "role": "assistant",
        "content": final_report
    })

    session["research_history"].append({
        "original_query": session["active_query"],
        "clarified_query": response.clarified_query,
        "report": final_report,
        "email_status": response.email_status,
        "status": "completed"
    })

    session["active_query"] = None
    session["active_messages"] = []

    yield (
        history,
        session,
        "Research completed!",
        ""
    )

def new_research(session):
    session = session or create_session()

    session["active_query"] = None
    session["active_messages"] = []
    session["awaiting_clarification"] = False

    return session, "Ready for a new research query."

with gr.Blocks() as ui:

    gr.Markdown("# AI Research Assistant")

    session = gr.State(create_session())

    chatbot = gr.Chatbot(
        label="Research Assistant",
        height=500
    )

    with gr.Row():
        query = gr.Textbox(
            placeholder="Enter your research query...",
            label="Your Query",
            scale=5
        )

        submit = gr.Button(
            "Send",
            variant="primary",
            scale=1
        )

    status = gr.Markdown("Ready to research.")

    new_button = gr.Button("New Research")

    submit.click(
        run_manager,
        inputs=[query, chatbot, session],
        outputs=[chatbot, session, status, query]
    )

    query.submit(
        run_manager,
        inputs=[query, chatbot, session],
        outputs=[chatbot, session, status, query]
    )

    new_button.click(
        new_research,
        inputs=[session],
        outputs=[session, status]
    )


ui.launch(
    theme=gr.themes.Default(primary_hue="sky")
)

