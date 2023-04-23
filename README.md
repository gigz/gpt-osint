# gpt-osint
## Team Members
- <a href="https://github.com/gigz">gigz</a>
- <a href="https://github.com/andrewasfa">andrewasfa</a>

## Tool Description

**gpt-osint** is a web-based tool that allows researchers to extract insights from various datasets, like social media/chat dumps, web pages, csv datasets and other documents using natural language queries. The main advantages of this tool include:
1. Effortless use across different langugages (e.g. Chinese chat log can be queried in plain English)
2. Ability to search for relevant data without the knowledge of exact keywords
3. Easy summarization or extraction of key information from large body of data

## Installation

### Web Hosted Tool

No installation required, just go to http://127.0.0.1:8080

### Local Version

1.  Make sure you have Python version 3.8 or greater installed

2.  Download the tool's repository using the command:

        git clone https://github.com/gigz/gpt-osint

3.  Move to the tool's directory and install the tool

        cd gpt-osint
        pip install .
        
4.  Specify your OpenAI API key:

        export OPENAI_API_KEY="<your_openai_api_key>"
       
    Alternatively you can create .env file and specify it there
    
    If you don't have OpenAI API key, you can subscribe to OpenAI platform <a href="https://platform.openai.com/">here</a>.

5.  [Optional] If you have access to gpt-4 and want to use it, specify it in GPT_MODEL environmental variable:

        export GPT_MODEL="gpt-4"
        
6.  Start wsgi server

        gunicorn app:app --bind 127.0.0.1:8080 --timeout 120
        
7.  In your web browser, go to http://127.0.0.1:8080 - that's it!

## Usage

The tool is straightforward to use. It requires just two inputs - a file or a set of files that researcher wants to analyze and a query written in any natural language.

As an input, the tool currently supports the following formats:

### Telegram Channel manual exports (JSON)

The **examples** folder contains a number of existing example files.

### Telegram Channel manual exports (JSON)

### Telegram Channel SNSCRAPE exports (JSONL)

- Follow the instructions from the repository: https://github.com/bellingcat/snscrape
- Use the command to export Telegram channel messages, like the following:

```
snscrape --jsonl --max-results 100 telegram-channel ssigny > ./examples/ssigny.jsonl

```

### Plaintext (txt, html)

### CSV


## Additional Information

This section includes any additional information that you want to mention about the tool, including:

- Potential next steps for the tool (i.e. what you would implement if you had more time)
- Any limitations of the current implementation of the tool
- Motivation for design/architecture decisions

---
