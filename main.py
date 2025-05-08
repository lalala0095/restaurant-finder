from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This FastAPI server is for backend of a Restaurant Finder App."}
