import hashlib
import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import List

import cachetools
import markdown
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.document_loaders import (CSVLoader, UnstructuredHTMLLoader,
                                        UnstructuredMarkdownLoader,
                                        UnstructuredPDFLoader)
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
gpt_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
llm = ChatOpenAI(model=gpt_model)
index_cache = cachetools.LRUCache(maxsize=100)

# This function reads a file in chunks and returns a SHA256 hash of the file
def files_hash_sha256(file_paths):
    sha256_hash = hashlib.sha256()
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            # Read the file in chunks to avoid using too much memory
            chunk_size = 8192
            file_chunk = file.read(chunk_size)
            while file_chunk:
                sha256_hash.update(file_chunk)
                file_chunk = file.read(chunk_size)
    return sha256_hash.hexdigest()

# The function below takes a dictionary as input and returns a string
def concatenate_rows(row: dict) -> str:
    date = row["date"]
    sender = row["from"]
    text = row["text"]
    return f"{sender} on {date}: {text}\n\n"

# Deals with annoying telegram richtext message format that breaks text down in chunks
# Some plan text, some dicts with type and text
def mp(message) -> str:
    if type(message) == str:
        return message
    else:
        ret = ""
        for x in message:
            if type(x) == str:
                ret += x
            elif x['type'] == 'bold' or x['type'] == 'italic':
                ret += x['text']
        return ret

# Loader for Telegram chat json directory dump
# Copypasted from Langchain and adopted to work with more than plaintext messages
class TelegramChatLoader(BaseLoader):
    """Loader that loads Telegram chat json directory dump."""

    def __init__(self, path: str):
        """Initialize with path."""
        self.file_path = path

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            import pandas as pd
        except ImportError:
            raise ValueError(
                "pandas is needed for Telegram loader, "
                "please install with `pip install pandas`"
            )
        p = Path(self.file_path)

        with open(p, encoding="utf8") as f:
            d = json.load(f)

        normalized_messages = pd.json_normalize(d["messages"])
        df_normalized_messages = pd.DataFrame(normalized_messages)

        # Only keep plain text messages (no services, links, hashtags, code, bold...)
        df_filtered = df_normalized_messages[
            (df_normalized_messages.type == "message")
            & (df_normalized_messages.text.apply(mp))
        ]

        df_filtered = df_filtered[["date", "text", "from"]]
        print(df_filtered[["text"]])

        text = df_filtered.apply(concatenate_rows, axis=1).str.cat(sep="")

        metadata = {"source": str(p)}

        return [Document(page_content=text, metadata=metadata)]

# Loader for telegram dump from snscraper
class TelegramScraperLoader(BaseLoader):
    """Loads JSONL files"""

    def __init__(self, path: str):
        """Initialize with path."""
        self.file_path = path

    def load(self) -> List[Document]:
        """Load documents."""
        try:
            import pandas as pd
        except ImportError:
            raise ValueError(
                "pandas is needed for Telegram loader, "
                "please install with `pip install pandas`"
            )
        p = Path(self.file_path)

        with open(p, mode='r') as f:
            json_list = list(f)

            data:list=[]

            for json_str in json_list:
                json_obj = json.loads(json_str)
                data.append({
                    "date":json_obj["date"],
                    "text":json_obj["content"]
                    })
                # content = json_obj['content'].encode('utf8')
            print("data", data)

            text = ''
            for post in data:
                text = ' '.join([text,"date:", post["date"], "text:", post["text"]or '' ])

        metadata = {"source": str(p)}

        return [Document(page_content=text, metadata=metadata)]


# Pick the right data loader based on file format
def get_loader(file):
    if file.endswith(".json"):
        return TelegramChatLoader(file)
    if file.endswith(".jsonl"):
        return TelegramScraperLoader(file)
    elif file.endswith(".html"):
        return UnstructuredHTMLLoader(file)
    elif file.endswith(".csv"):
        return CSVLoader(file)
    elif file.endswith(".pdf"):
        return UnstructuredPDFLoader(file, mode="elements")
    elif file.endswith(".txt"):
        return UnstructuredMarkdownLoader(file)
    else:
        raise ValueError(f"Unknown file type {file}")

# This function build index from telegram chat file and using langchain
# Creates two hop query - gets data from index and then sends prompt to gpt
def get_completion(files, question):
    f_hash = files_hash_sha256(files)
    if f_hash in index_cache:
        db = index_cache[f_hash]
    else:
        loaders = [get_loader(file) for file in files]
        documents = [loader.load() for loader in loaders]
        documents = [doc for docs in documents for doc in docs]
        texts = text_splitter.split_documents(documents)
        db = FAISS.from_documents(texts, embeddings)
        index_cache[f_hash] = db
    retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    return qa.run(question)
    
# Saves uploaded files, sends first for indexing
def process_files(files, question):
    file_paths = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            file_paths.append(file_path)

        response = get_completion(file_paths, "Try to give answers with context and message timestamps. " + question)

    return response

# Flask endpoints
@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        try:
            files = request.files.getlist("json_files")
            question = request.form["question"]
            print("POST request:", files, question)
            answer = process_files(files, question)
            print("Response:", answer)
            answer_html = markdown.markdown(answer)
            return render_template(
                "result.html",
                question=question,
                answer_html=answer_html)
        except Exception as e:
            print(e)  # This will print the exception details to the console, remove if not needed
            flash('Error: ' + str(e), 'error')

    print("GET request")
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)