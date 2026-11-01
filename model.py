from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, set_tracing_disabled
import os

load_dotenv(override=True)
set_tracing_disabled(True)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = os.getenv("GOOGLE_API_KEY")
Gemini_model = "gemini-3.5-flash-lite"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
OpenRouter_model = "liquid/lfm-2.5-2.6b:free"

openrouter_client = AsyncOpenAI(base_url=OPENROUTER_BASE_URL, api_key=openrouter_api_key)

openrouter_model = OpenAIChatCompletionsModel(model=OpenRouter_model, openai_client=openrouter_client)

gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)

gemini_model = OpenAIChatCompletionsModel(model=Gemini_model, openai_client=gemini_client)
