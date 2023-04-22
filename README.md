## Install Dependencies

```
pip install -r requirements.txt
```

## Launch

```
export OPENAI_API_KEY="<your openai key sk-xxxxx>"
gunicorn app:app --bind 127.0.0.1:8080 --timeout 120
```
