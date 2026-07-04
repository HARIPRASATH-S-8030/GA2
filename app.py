# /// script
# requires-python = ">=3.11"
# dependencies = [
#      "fastapi",
#      "uvicorn",
# ]
# ///

from fastapi import FastAPI, HTTPException, Query, Request, Response
import time
import uuid

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-55nz6e.example.com"

@app.middleware("http")
async def cors_and_custom_headers_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("Origin")
    
    # --- 1. HANDLE PREFLIGHT OPTIONS EXPLICITLY ---
    if request.method == "OPTIONS":
        if origin == ALLOWED_ORIGIN:
            response = Response(status_code=200)
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Request-ID, X-Process-Time"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        else:
            # Strictly REJECT invalid origins with a 400 Bad Request and NO ACAO header
            response = Response(content="CORS Origin Not Allowed", status_code=400)
        
        # Every response must carry these tracking headers
        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

    # --- 2. EXECUTE CORE API LOGIC ---
    response = await call_next(request)
    
    # --- 3. APPLY GET CORS RULES ---
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    # --- 4. STAMP MANDATORY HEADERS ON EVERY RESPONSE ---
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    response.headers["Access-Control-Expose-Headers"] = "X-Request-ID, X-Process-Time"
    
    return response

@app.get("/stats")
async def calculate_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        parsed_values = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input integers.")

    if not parsed_values:
        raise HTTPException(status_code=400, detail="No values provided.")

    count = len(parsed_values)
    total_sum = sum(parsed_values)
    min_val = min(parsed_values)
    max_val = max(parsed_values)
    mean_val = total_sum / count

    return {
        "email": "24f1001287@ds.study.iitm.ac.in",
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": round(mean_val, 4)
    }

@app.get("/")
async def root():
    return {"message": "Stats API is live."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)