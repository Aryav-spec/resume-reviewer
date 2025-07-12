import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import faiss

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"

def get_embedding(text):
    response = client.embeddings.create(input=[text], model=EMBED_MODEL)
    return response.data[0].embedding

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
