# -*- coding: utf-8 -*-
"""Rag.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19Xqo_wW4MiYooAcDd-TmPhb22Lfo_jXr
"""

## load google drigve

from google.colab import drive
drive.mount("/content/drive")

# !pip install langchain chromadb langchain_community pypdf sentence-transformers llama-cpp-python

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA , LLMChain
from langchain_community.llms import LlamaCpp

loader = PyPDFDirectoryLoader("/content/drive/MyDrive/10thbook")

books = loader.load()

len(books)

recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = recursive_splitter.split_documents(books)

len(chunks)

import os

os.environ["HUGGINGFACE_API_TOKEN"] = "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"

embeddings =SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(chunks,embeddings)

query = "Explain some direct and indirect taxes"

search_results = vector_store.similarity_search(query)

search_results

retriever = vector_store.as_retriever(search_kwargs={"k":5})
retriever.get_relevant_documents(query)

# !pip install huggingface_hub

# !pip install -U bitsandbytes

# !pip install langchain_huggingface
# !pip install huggingface_hub



from langchain_huggingface import HuggingFaceEndpoint

repo_id = "justsomerandomdude264/SocialScience_Homework_Solver_Llama318B"

llm = HuggingFaceEndpoint(repo_id=repo_id, token="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")



pip install -U bitsandbytes

llm = LlamaCpp(
    model_path="/content/drive/MyDrive/10thbook/Mistral-7B-Instruct-v0.3.Q4_K_S.gguf",
 temperature=0.2,
           max_tokens=2048,
           top_p=1
)

from google.colab import drive
drive.mount('/content/drive')

templates = """
<|context|>
you are an social science assistant who follows the instruction and generate the response based on the query and the content provided , please be truthful and give direct answers
</s>
<|user|>
{query}
</s>
<|assistant|>
"""

from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(templates)

rag_chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("Explain some direct and indirect taxes")
response

response

GOOGLE_DRIVE_PATH = "/content/drive/MyDrive/10thbook/" #@param {type:"string"}
REPO_ID = "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF" #@param {type:"string"}
FILE_NAME = "Mistral-7B-Instruct-v0.3.Q4_K_S.gguf" #@param {type:"string"}

from huggingface_hub import hf_hub_download
filePath = hf_hub_download(repo_id=REPO_ID, filename=FILE_NAME, cache_dir="/content/hfcache")
print(filePath)

# !cp $filePath $GOOGLE_DRIVE_PATH
# !ls $GOOGLE_DRIVE_PATH

# !cd /content/drive/MyDrive/10thbook
# !du /content/drive/MyDrive/10thbook/Mistral-7B-Instruct-v0.3.Q4_K_S.gguf -h