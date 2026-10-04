from fastapi import FastAPI

app = FastAPI(title="Face Attendance API")


@app.get("/health")
def health():
    return {"status": "ok"}