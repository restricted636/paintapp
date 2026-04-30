from fastapi import FastAPI
from datetime import datetime, timezone
from database import init_db
from routers import user_router, palette_router, color_router

app = FastAPI(title="PaintApp API")

# Initialize database tables
init_db()

# Include routers
app.include_router(user_router)
app.include_router(palette_router)
app.include_router(color_router)


@app.get("/")
def root():
    return {"message": "PaintApp API is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "utc_time": datetime.now(timezone.utc).isoformat()
    }