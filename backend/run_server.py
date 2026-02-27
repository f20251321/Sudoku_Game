"""
Script to run the FastAPI server.
Run from the backend directory: python run_server.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
