# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi",
#     "uvicorn",
# ]
# ///

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()

# Your strictly allowed CORS origin assigned by the grader
ALLOWED_ORIGIN = "https://dash-55nz6e.example.com"

# FastAPI's CORSMiddleware automatically handles preflight OPTIONS 
# and sets Access-Control-Allow-Origin only for this explicit origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Custom middleware to add X-Request-ID and X-Process-Time to EVERY response
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    
    # Generate a unique tracking UUID for this specific request
    request_id = str(uuid.uuid4())
    
    # Process the request down the line
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.time() - start_time
    
    # Attach required custom headers to the outgoing response
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

@app.get("/stats")
async def calculate_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        # Parse the comma-separated string into actual Python integers
        parsed_values = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid input. Ensure the values parameter contains only integers separated by commas."
        )

    if not parsed_values:
        raise HTTPException(
            status_code=400, 
            detail="No values provided to calculate statistics."
        )

    # Compute descriptive statistics dynamically
    count = len(parsed_values)
    total_sum = sum(parsed_values)
    min_val = min(parsed_values)
    max_val = max(parsed_values)
    mean_val = total_sum / count

    return {
        "email": "24f1001287@ds.study.iitm.ac.in",  # <-- REPLACE WITH YOUR ACTUAL ASSIGNMENT EMAIL
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": round(mean_val, 4)  # Safely within the ±0.01 requirement
    }

@app.get("/")
async def root():
    return {"message": "Stats API is live. Use /stats?values=1,2,3"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)