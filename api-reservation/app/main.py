from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bonjour — petite API prête", "time": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
