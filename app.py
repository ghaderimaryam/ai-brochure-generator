import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_contents
import gradio as gr

# ── Environment setup ──────────────────────────────────────────────────────────

load_dotenv(override=True)

# The following clients are configured for future use or alternative routing.
# Claude is currently accessed via OpenRouter; Anthropic and Gemini clients
# are kept here for easy switching between providers without code changes.

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if openrouter_api_key:
    print(f"OpenRouter API Key exists and begins {openrouter_api_key[:3]}")
else:
    print("OpenRouter API Key not set (this is optional)")

# ── Constants ──────────────────────────────────────────────────────────────────

SYSTEM_MESSAGE = """
You are an assistant that analyzes the contents of a company website landing page
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
"""

# ── API Clients ────────────────────────────────────────────────────────────────

# OpenAI client (GPT models)
openai = OpenAI(api_key=openai_api_key)

# Claude is accessed via OpenRouter using the OpenAI-compatible interface
openrouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

# ── Streaming functions ────────────────────────────────────────────────────────

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": prompt}
    ]
    stream = openai.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_claude(prompt):
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": prompt}
    ]
    stream = openrouter.chat.completions.create(
        model='anthropic/claude-sonnet-4.5',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_model(prompt, model):
    if model == "GPT":
        yield from stream_gpt(prompt)
    elif model == "Claude":
        yield from stream_claude(prompt)
    else:
        raise ValueError(f"Unknown model: {model}")


# ── Main brochure function ─────────────────────────────────────────────────────

def stream_brochure(company_name, url, model):
    yield ""

    if not company_name.strip() or not url.strip():
        yield "Please provide both a company name and a URL."
        return

    try:
        page_content = fetch_website_contents(url)
        prompt = (
            f"Please generate a company brochure for {company_name}. "
            f"Here is their landing page:\n\n{page_content}"
        )
        yield from stream_model(prompt, model)
    except Exception as e:
        yield f"Something went wrong: {e}"


# ── Gradio UI ──────────────────────────────────────────────────────────────────

view = gr.Interface(
    fn=stream_brochure,
    title="AI Brochure Generator",
    inputs=[
        gr.Textbox(label="Company name:"),
        gr.Textbox(label="Landing page URL including http:// or https://"),
        gr.Dropdown(["GPT", "Claude"], label="Select model", value="GPT")
    ],
    outputs=[gr.Markdown(label="Response:")],
    examples=[
        ["Hugging Face", "https://huggingface.co", "GPT"],
        ["Edward Donner", "https://edwarddonner.com", "Claude"]
    ],
    allow_flagging="never"
)

view.launch(inbrowser=True)