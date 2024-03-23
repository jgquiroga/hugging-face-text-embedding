import time
from typing import List
from fastapi import FastAPI, HTTPException, Request
from starlette.datastructures import MutableHeaders
from pydantic import BaseModel
import uvicorn
import logging

logging.basicConfig(level = logging.INFO)
log = logging.getLogger("app")

from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Create a new FastAPI app instance
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def add_default_content_type(request: Request, call_next):
    new_header = MutableHeaders(request.headers)
    new_header['Content-Type'] = str("application/json")
    request.scope.update(headers = new_header.raw)
    response = await call_next(request)
    return response

# Input definition
class Inputs(BaseModel):
    '''
    List of sentences to calculate embeddings
    '''
    inputs: List[str] = ["sentence 1", "sentence 2"]

class SKEmbeddingVector(BaseModel):
    embedding: list[float]

class SKResponse(BaseModel):
    '''
    List of embeddings in Semantic Kernel Format
    '''
    data: List[SKEmbeddingVector]

# Model used for the embeddings
# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@app.post("/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2")
async def generateEmbeddings(inputs: Inputs) -> list[list[list[list[float]]]]:
    '''
    Generates a list of embeddings using the model: sentence-transformers/all-MiniLM-L6-v2
    This model returns vectors of 384 dimensions
    '''
    try:
        log.debug("Receiving input sentences")
        embeddings = model.encode(inputs.inputs)
        result = []
        rows = []
        result.append(rows)
        for output in embeddings:
            row = []
            vector = []
            for embedding in output:
                vector.append(embedding)
            row.append(vector)
            rows.append(row)

        log.debug("Returning embedding vectors")
        return result
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=500, detail="An error has ocurred")

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8080, host="0.0.0.0")