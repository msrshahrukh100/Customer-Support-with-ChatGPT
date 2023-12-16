from fastapi import FastAPI
from utils import get_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def read_item(q: str):
    print(f"received query with q: {q}")
    openai_response = get_response(q)
    return {"text": openai_response}