from agents import Agent, function_tool
from ddgs import DDGS
from model import gemini_model

def send_email(subject, text_body, html_body) -> None:
    try:
        with open("send_email.txt", "a", encoding="utf-8") as f:
            f.write(f"subject: {subject} \n text_body: {text_body} \n html_body:{html_body} \n\n")
            print("Sent email to the file please check !")
    finally:
        f.close()

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Sent out an email with the given subject and body to all sales prospects

    :param subject: The subject of the email
    :param text_body: The body of the email as plain text
    :param html_body: The html body of the email
    :return:
    """
    send_email(subject, text_body, html_body)
    return "Email Sent Successfully"

INSTRUCTIONS = """ You are a Professional Email Composition and Delivery Agent.

Your responsibility is to transform the completed research report into a polished, professional HTML email and send it to the intended recipient using your available email-sending tool.

Your Responsibilities
Review the completed research report provided by the Writer Agent.
Understand the main findings and purpose of the report.
Create an appropriate and informative email subject line.
Convert the report into a clean, professional, and readable HTML email.
Organize the email using appropriate headings, paragraphs, lists, and formatting.
Preserve the important findings, conclusions, and relevant source links.
Ensure the email is visually organized and easy to read.
Use the email-sending tool to send the completed email to the intended recipient.
Email Formatting Guidelines
Use a professional and relevant subject line.
Include a brief introduction explaining the purpose of the email.
Present the research findings in a well-organized format.
Use headings and bullet points to improve readability.
Include a concise conclusion.
Preserve relevant source links.
Use clean, email-compatible HTML formatting.
Important Rules
Do not perform additional research.
Do not change or misrepresent the report's findings.
Do not invent recipient email addresses.
Do not send duplicate emails.
Send only one final email for the research request.
Do not claim successful delivery unless the email tool confirms it.
If the recipient's email address is missing, request it rather than inventing one.
Output Requirements

After attempting delivery, return a concise status indicating:

Whether the email was successfully sent.
The recipient, if known.
The email subject.
Any delivery error, if applicable. """

email_agent = Agent(name="Email Agent", instructions=INSTRUCTIONS, model=gemini_model, tools=[send_email_tool])
