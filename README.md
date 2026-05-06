# AgenticAI — AI Website Cloning CLI Agent

An AI-powered CLI agent that can generate responsive websites directly from natural language prompts using step-by-step reasoning and tool execution.

This project simulates how modern AI coding agents like Cursor or Windsurf operate inside the terminal.

---

# Features

- Conversational terminal-based AI agent
- Step-by-step reasoning loop
- Tool calling architecture
- AI-generated HTML, CSS and JavaScript
- Automatic folder and file creation
- Responsive landing page generation
- OpenRouter LLM integration
- Mobile responsive layouts
- Smooth scrolling + hamburger menu support

---

# Agent Workflow

The agent operates using a reasoning loop:

```text
START → THINK → TOOL → OBSERVE → OUTPUT
```

Instead of generating everything at once, the agent:
1. Thinks about the next action
2. Uses tools
3. Observes the result
4. Continues iteratively until the website is complete

---

# Available Tools

| Tool | Description |
|---|---|
| create_folder | Creates project folders |
| write_file | Writes HTML/CSS/JS files |
| read_file | Reads existing files |
| open_browser | Opens generated webpage |

---

# Tech Stack

- Python
- OpenRouter API
- OpenAI SDK
- Asyncio
- HTML
- CSS
- JavaScript

---

# Project Structure

```text
AgenticAI/
│
├── main.py
├── .env
├── requirements.txt
│
└── scaler/
    ├── index.html
    ├── style.css
    └── index.js
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/Karthikeya914/AgenticAI.git

cd AgenticAI
```

---

## 2. Create Virtual Environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install openai python-dotenv
```

---

## 4. Add API Key

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Get your API key from:
https://openrouter.ai/workspaces/default/keys

---

# Run the Agent

```bash
python main.py
```

---

# Example Prompt

```text
Create a modern responsive landing page inspired by Scaler Academy. Create a folder named scaler with exactly 3 files: index.html, style.css and index.js. The page should have a sticky navbar, bold hero section, feature cards, CTA buttons, dark blue theme, responsive layout and mobile hamburger menu.
```

---

# Sample Output

The agent generates:

- Responsive landing page
- Sticky navigation bar
- Hero section
- Feature cards
- Footer
- Mobile responsive menu
- Modern UI styling

---

# Assignment Objective

This project was built as part of an AI Agent CLI Tool assignment.

The goal was to:
- Build a conversational CLI agent
- Accept natural language instructions
- Generate real website files
- Clone a Scaler-like landing page
- Demonstrate agentic reasoning and tool execution

---

# Demo Video

Add your YouTube demo link here:

```text
https://youtu.be/X_r2WC4arr8
```

---

# Future Improvements

- Browser automation support
- Real website scraping
- Multi-page generation
- React/Tailwind support
- Streaming responses
- File diff editing
- Agent memory

---

# Author

Karthikeya  
GitHub: https://github.com/Karthikeya914
