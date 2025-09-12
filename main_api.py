from fastapi import FastAPI
from main import logic
app = FastAPI()

@app.get("/")
def val():
    return {"ans": logic() }
