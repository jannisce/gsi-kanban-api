from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
from app.routers import board_router, list_router, task_router

app = FastAPI(title="Kanban API")

# Health Check
@app.get("/health", tags=["health"], status_code=200)
def health_check():
    formatted_time = datetime.now(timezone(timedelta(hours=-6))).strftime("%H:%M:%S %Y-%m-%d")
    return {"status": f"ok", "timestamp": formatted_time}

# Routers
app.include_router(board_router)
app.include_router(list_router)
app.include_router(task_router)
