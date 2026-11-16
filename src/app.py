import os

from fastapi import FastAPI

app = FastAPI(title="doc-sync demo")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


@app.get("/version")
def version() -> dict[str, str]:
    return {
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development"),
        "region": os.getenv("APP_REGION", "local"),
    }
