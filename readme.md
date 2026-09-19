# Python AI Toolkit
A lightweight command-line AI toolkit built with Python and the Google Gemini API. It provides AI-powered utilities for text summarization, translation, and sentiment analysis directly from the terminal.

## Features
- 📝 **Summarization** — Convert text into concise bullet points.
- 🌐 **Translation** — Translate text into different languages.
- 💭 **Sentiment Analysis** — Classify text as `POSITIVE`, `NEGATIVE`, or `NEUTRAL`.
- 🔄 **Automatic Retry** — Retries temporary API failures using exponential backoff.
- ⏳ **Terminal Spinner** — Displays a loading animation while Gemini processes the request.
- 🔐 **Environment Variables** — Keeps the Gemini API key outside the source code.
- 🧩 **Object-Oriented Design** — Separates CLI handling, prompt generation, API communication, and response display.

## Tech Stack
- Python
- Google Gemini API
- Google GenAI SDK
- python-dotenv
- argparse
- threading

## Project Structure
```text
python-ai-toolkit/
│
├── ai_toolkit.py
├── .env
├── .gitignore
└── README.md
```

## Installation
### Clone the Repository
```bash
git clone https://github.com/your-username/python-ai-toolkit.git
cd python-ai-toolkit
```

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```
**macOS/Linux:**
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install google-genai python-dotenv
```

## API Configuration
Create a `.env` file in the project root:
```env
API_KEY=your_gemini_api_key
```
Add `.env` to `.gitignore` to prevent accidentally committing your API key:
```gitignore
.env
__pycache__/
venv/
```

## Usage
### Summarization
```bash
python ai_toolkit.py --task summarize --text "Artificial intelligence is transforming modern software development by automating repetitive tasks and improving developer productivity."
```

### Translation
```bash
python ai_toolkit.py --task translate --lang hindi --text "Artificial intelligence is changing the world."
```
You can replace `hindi` with any supported target language.

### Sentiment Analysis
```bash
python ai_toolkit.py --task sentiment --text "I really enjoyed this product."
```
Example output:
```text
POSITIVE
```

## Available Tasks
| Task | Command | Description |
|---|---|---|
| Summarization | `--task summarize` | Summarizes the provided text |
| Translation | `--task translate` | Translates text into the specified language |
| Sentiment Analysis | `--task sentiment` | Classifies the sentiment of the text |

For translation, specify the target language with:
```bash
--lang <language>
```

## Architecture
The project follows a modular Object-Oriented Programming architecture:
```text
                    AIToolkit
                        │
            ┌───────────┴───────────┐
            │                       │
       CLIHandler             PromptBuilder
            │                       │
            └───────────┬───────────┘
                        │
                  GeminiClient
                        │
                     Spinner
                        │
                   Gemini API
                        │
                        ↓
                ResponseDisplay
```

### `AIToolkit`
The main application class that coordinates the complete workflow.

### `CLIHandler`
Handles command-line arguments and input validation using `argparse`.

### `PromptBuilder`
Creates task-specific prompts for:
- Summarization
- Translation
- Sentiment analysis

### `GeminiClient`
Handles communication with the Gemini API and manages retry logic for temporary API failures.

### `Spinner`
Provides a terminal loading animation while the API request is being processed.

### `ResponseDisplay`
Formats and displays the generated Gemini response in the terminal.

## Retry Strategy
The toolkit automatically retries temporary API failures using exponential backoff.

### Retryable Status Codes
```text
408
429
500
502
503
504
```

### Retry Sequence
```text
Attempt 1 → wait 1 second
Attempt 2 → wait 2 seconds
Attempt 3 → wait 4 seconds
```
The maximum number of attempts is `3`.

## Error Handling
The application handles:
- Missing API keys
- Empty input
- Invalid tasks
- Temporary API failures
- Server errors
- Keyboard interruption

Example:
```text
Error: API_KEY is missing from your .env file.
```

## Security
The Gemini API key is stored in an environment variable:
```env
API_KEY=your_gemini_api_key
```
Do not hard-code API keys in the source code.
```python
# ❌ Avoid this
client = genai.Client(api_key="your-api-key")
```
Use environment variables instead:
```python
# ✅ Recommended
api_key = os.getenv("API_KEY")
```

## Future Improvements
- [ ] Add question-answering
- [ ] Add keyword extraction
- [ ] Add grammar correction
- [ ] Add code generation
- [ ] Add conversation mode
- [ ] Add streaming responses
- [ ] Add unit tests
- [ ] Add logging
- [ ] Add configuration file support
- [ ] Support multiple Gemini models

## Learning Goals
This project was built to practice:
- Python OOP
- API integration
- CLI application development
- Environment variable management
- Exception handling
- Retry mechanisms
- Multithreading
- Prompt engineering
- Modular software design

## License
This project is intended for learning and educational purposes.

## Author
**Sushil Kumar Sahoo**

B.Sc. Computer Science Student | Aspiring Data Scientist & AI Engineer