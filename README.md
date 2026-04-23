# AI Brochure Generator

Automatically generates a professional company brochure by scraping a website's 
landing page and passing it to an LLM (GPT-4 or Claude). Built with Python and Gradio.

## Demo

![Demo](assets/demo.gif)

## Features

- Scrapes any company landing page
- Generates a structured markdown brochure
- Supports GPT-4.1-mini and Claude (via OpenRouter)
- Streams the response in real time
- Clean Gradio UI with example inputs

## Tech Stack

- Python
- OpenAI API / OpenRouter API
- Gradio
- BeautifulSoup / requests (scraper)

## Getting Started

### 1. Clone the repo
git clone https://github.com/yourusername/ai-brochure-generator.git
cd ai-brochure-generator

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set up environment variables
cp .env.example .env
# Fill in your API keys in .env

### 4. Run the app
python app.py
