from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()

EMAIL = "24f1001287@ds.study.iitm.ac.in"

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-55nz6e.example.com"
    ],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# Middleware for Request ID and Process Time
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/stats")
def stats(values: str):
    try:
        nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integer values")

    if not nums:
        raise HTTPException(status_code=400, detail="No values provided")

    total = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums)
    }