from fastapi import FastAPI

app = FastAPI(
    title="Antonmazur API",
    description="My FastAPI application",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello from Antonmazur!", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": "Antonmazur"}

@app.get("/info")
async def get_info():
    return {
        "name": "Antonmazur",
        "version": "0.1.0",
        "framework": "FastAPI"
    }
