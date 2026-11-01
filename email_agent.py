import os
import smtplib
from email.message import EmailMessage

from agents import Agent, function_tool
from model import gemini_model


def send_email(subject: str, text_body: str, html_body: str, recipient: str) -> str:
    """Send an email when SMTP is configured; otherwise save a draft locally."""
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("EMAIL_FROM", smtp_username or "")

    if not all((smtp_host, sender, recipient)):
        with open("send_email.txt", "a", encoding="utf-8") as draft_file:
            draft_file.write(
                f"To: {recipient}\nSubject: {subject}\n"
                f"Text body:\n{text_body}\nHTML body:\n{html_body}\n\n"
            )
        return "SMTP is not fully configured; email draft saved to send_email.txt."

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.send_message(message)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.send_message(message)

    return f"Email sent successfully to {recipient}."


@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str, recipient: str) -> str:
    """Send the report email to the recipient, or save a draft if SMTP is not configured."""
    try:
        return send_email(subject, text_body, html_body, recipient)
    except Exception as exc:
        return f"Email delivery failed: {type(exc).__name__}: {exc}"


INSTRUCTIONS = """You are a professional email composition and delivery agent.

Transform the completed research report into a clear, professional email. Preserve the report's findings and source links. Use the recipient address supplied by the user; never invent an address. If email delivery was requested but the recipient address is missing, ask for it before calling the tool. Do not send duplicate emails.

The email tool sends the message through SMTP when configured. If SMTP is not fully configured, it saves a draft to send_email.txt and reports that it saved a draft. Report the tool's result accurately; never claim delivery when only a draft was saved or when delivery failed.
"""

email_agent = Agent(
    name="Email Agent",
    instructions=INSTRUCTIONS,
    model=gemini_model,
    tools=[send_email_tool],
)
