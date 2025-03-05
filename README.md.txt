# FRIDAY - AI-Powered Virtual Assistant

## Overview

FRIDAY is a Python-based AI assistant capable of handling various automation tasks, including real-time search, AI-based chatbot interactions, image generation, speech recognition, and text-to-speech conversion. The assistant integrates multiple APIs and services to provide a seamless experience.

## Features

- Speech Recognition
- AI Chatbot (LLM Integration)
- Real-Time Search Engine
- AI Image Generation
- Text-to-Speech Conversion
- Task Automation

## Installation & Setup

Follow these steps to set up FRIDAY on your local machine.

### Step 1: Install Python 3.10.10

Ensure you have Python 3.10.10 installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/release/python-31010/).

### Step 2: Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv friday_env
```

Activate the virtual environment:

- **Windows**:
  ```bash
  friday_env\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source friday_env/bin/activate
  ```

### Step 3: Install Dependencies

Use the following command to install all required dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

Some features require API keys (e.g., OpenAI, Hugging Face, Cohere, Groq). Store them in the `.env` file under the `config/` directory. Example:

```
OPENAI_API_KEY=your_api_key_here
HUGGINGFACE_API_KEY=your_api_key_here
COHERE_API_KEY=your_api_key_here
GROQ_API_KEY=your_api_key_here
```

You can obtain API keys from the following sources:
- [Hugging Face](https://huggingface.co/join)
- [Cohere](https://cohere.com/signup)
- [Groq](https://console.groq.com/signup)

### Step 5: Run FRIDAY

Once everything is set up, run the main script:

```bash
python main.py
```

## Usage

- Use voice commands to interact with FRIDAY.
- AI chatbot handles general queries.
- Image generation feature utilizes AI-based APIs.
- Search engine retrieves real-time information from the web.

## Tech Stack

- **Python 3.10.10**
- **SpeechRecognition** (Speech-to-Text)
- **OpenAI API** (LLM & Image Generation)
- **Pyttsx3** (Text-to-Speech)
- **Other required libraries in** `requirements.txt`

## Credits

This project was created by **Vijay BV**.

Special thanks to **Kaushik Shresth** for providing valuable insights and guidance through YouTube tutorials.

Additional references:
- Various online sources, including YouTube, Google, and ChatGPT, were used to understand and implement features.

## Contributing

This project is not open for contributions at the moment.

## License

Copyright (c) 2025 Vijay.BV

Permission is hereby granted, free of charge, to any person obtaining a copy of this software...

