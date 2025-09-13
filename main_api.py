from fastapi import FastAPI
from main import logic
import json
app = FastAPI()

@app.get("/")
def val():
    return {"ans": logic() }
