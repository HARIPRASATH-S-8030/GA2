from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import time
import uuid

app = FastAPI()

EMAIL = "24f1001287@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-55nz6e.example.com"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def process_time(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(time.perf_counter() - start)

    return response


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/stats")
def stats(values: str):

    nums = [int(x) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums)
    }