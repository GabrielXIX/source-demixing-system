from fastapi import FastAPI, HTTPException

# use pydantic?
app = FastAPI()


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/split")
def split_audio(audio_file):
    # logic for separation
    return "a"
