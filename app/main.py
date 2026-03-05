from fastapi import FastAPI
from app.api import tour, vision

app = FastAPI(title="AI Tourism Guide")

app.include_router(tour.router)
app.include_router(vision.router)

@app.get("/")
def health():
    return {"status": "AI Tour Guide running"}
