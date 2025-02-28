from fastapi import FastAPI
from datetime import datetime, timezone, timedelta

app = FastAPI(title="Kanban API")

# Health Check
@app.get("/health", tags=["health"], status_code=200)
def health_check():
    formatted_time = datetime.now(timezone(timedelta(hours=-6))).strftime("%H:%M:%S %Y-%m-%d")
    return {"status": f"ok", "timestamp": formatted_time}
