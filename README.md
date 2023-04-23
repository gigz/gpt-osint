## Install Dependencies

```
pip install -r requirements.txt
```

## Launch

```
export OPENAI_API_KEY="<your openai key sk-xxxxx>"
gunicorn app:app --bind 127.0.0.1:8080 --timeout 120
```


## Get data to analyse
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
