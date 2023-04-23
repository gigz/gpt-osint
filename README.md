# gpt-osint
## Team Members
- <a href="https://github.com/gigz">gigz</a>
- <a href="https://github.com/andrewasfa">andrewasfa</a>

## Tool Description

**gpt-osint** is a web-based tool that allows researchers to quickly extract insights from various datasets, like social media/chat dumps, web pages, csv datasets and other documents using natural language queries. The main advantages of this tool are:
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

As a file input, the tool currently supports the following formats:

- **Telegram Channel manual exports (json)**
 
  Export a telegram channel or chat as a json file manually (<a href="https://www.maketecheasier.com/export-telegram-chat-history">instructions</a>)

- **Telegram Channel SNSCRAPE exports (jsonl)**

  1. Follow the instructions from the snscrape repository: https://github.com/bellingcat/snscrape
  2. Use the command to export Telegram channel messages, like the following:

         snscrape --jsonl --max-results 100 telegram-channel ssigny > ./examples/ssigny.jsonl

- **Web Page (html)**
 
  From the web browser, save the page as plain html.

- **Tabular Data (csv)**
 
  Bring in your own csv file!

- **Other Formats**
 
  Currently not supported, however <a href="https://python.langchain.com/en/latest/modules/indexes/document_loaders.html">many</a> can be vert easily added.

You can select one or more files by clicking **"Select Files"** button.

After selecting files, specify your question. It can be anything like: "Summarize the events that happened yesterday", "Does this chat mentions person X and in what context", "What is the opinion of channel owner on topic Y".

Press **"Submit"** and wait for the answer to come up (can take a while, up to a minute in some cases, so please be patient)!

### Examples
The <a href="https://github.com/gigz/gpt-osint/tree/main/examples">examples</a> folder contains a number of existing files in different formats.

### Limitations

Currently there are certain limitaions on the file size. While the actual limit depends on the number of text tokens in the file, the reasonable approximation is **1mb** for gpt-3 processing (default) and **10mb** for gpt-4 processing.

## Additional Information

This tool is currently just a proof of concept and an attempt to validate how useful large language models can be in osint research. There are clearly some superpowers that LLMs bring to the table, like ability to operate across language, ability to retrieve information without knowing keywords or ability to summarize and extract key facts. At the same point, there are some obvious disadvanteges, like non-deterministic behavior of the model (can easily miss data, can even make things up). Whether these disadvanges are too sever to render the approach not useful is remain to be seen.

The current version of the tool is implemented with the state of the art but proprietary technology (OpenAI's gpt-4). It also has additional limitations stemming from the fact that gpt plug-ins are not widely available now and hence the significant restrictions on the dataset size being analyzed. It is likely, however, that emerging publicly available models (like <a href="https://ai.facebook.com/blog/large-language-model-llama-meta-ai/">llama</a>/<a href="https://crfm.stanford.edu/2023/03/13/alpaca.html">alpaca</a>) will get reasonably close to gpt-4 quality-wise within next few months and advancements of frameworks like <a href="https://python.langchain.com/en/latest/index.html">LangChain</a> will enable much more sophisticated workflows with LLMs.

And finally, here is what gpt-4 itself thinks about its usefulness for the osint community:

>Large language models, like ChatGPT, can be valuable tools for OSINT (Open Source Intelligence) researchers in various ways. They can help gather, analyze, and synthesize information from publicly available sources, making the research process more efficient and effective. Some of the ways large language models can assist OSINT researchers include:
>
>- Data aggregation: Language models can help gather information from multiple sources, such as news articles, social media, public databases, and forums, and present the data in a structured manner.
>
>- Language translation: These models can provide real-time translations of content in different languages, enabling researchers to access and understand information from diverse sources without language barriers.
>
>- Sentiment analysis: Language models can analyze text to determine sentiment, which can help OSINT researchers understand public opinion on various topics, track sentiment shifts over time, and identify potential threats or emerging trends.
>
>- Entity recognition and extraction: Large language models can automatically recognize and extract information about key entities, such as people, organizations, and locations, making it easier for researchers to track and analyze relevant data.
>
>- Summarization: Researchers often need to review massive amounts of information, and language models can help by providing concise summaries of long documents or articles, saving time and making the research process more efficient.
>
>- Relationship mapping: Language models can help identify relationships between various entities and topics, revealing connections that might not be apparent at first glance.
>
>- Trend analysis and prediction: These models can analyze historical data and identify patterns or trends, which can be helpful in predicting future events or anticipating potential risks.
>
>- Anomaly detection: By analyzing large volumes of data, language models can help identify unusual patterns or activities that may warrant further investigation.
>
>- Automated reporting: Language models can generate reports or briefings based on the collected data, making it easier for researchers to share findings with stakeholders.
>
>- Knowledge management: Large language models can help OSINT researchers manage their accumulated knowledge by creating searchable databases, categorizing information, and keeping track of ongoing developments.
>
>However, it's crucial to remember that large language models may have limitations in terms of accuracy, bias, and the potential to be manipulated. OSINT researchers should always verify information and combine the insights from language models with other research methods and tools to ensure the most accurate and reliable results.
