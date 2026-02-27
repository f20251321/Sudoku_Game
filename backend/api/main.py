"""
FastAPI main application.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from sudoku.solver import SudokuSolver
from sudoku.generator import SudokuGenerator
from ocr.image_processor import SudokuOCR

app = FastAPI(title="Sudoku Arena API")

# CORS middleware
frontend_url = os.environ.get("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    difficulty: str = "medium"


class GenerateResponse(BaseModel):
    puzzle: List[List[int]]
    solution: List[List[int]]


class SolveRequest(BaseModel):
    grid: List[List[int]]


class SolveResponse(BaseModel):
    solved: bool
    solution: Optional[List[List[int]]] = None
    error: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Sudoku Arena API"}


@app.post("/api/generate/", response_model=GenerateResponse)
def generate_puzzle(request: GenerateRequest):
    """Generate a Sudoku puzzle with specified difficulty."""
    try:
        generator = SudokuGenerator()
        puzzle, solution = generator.generate(request.difficulty.lower())
        return GenerateResponse(puzzle=puzzle, solution=solution)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating puzzle: {str(e)}")


@app.post("/api/solve/", response_model=SolveResponse)
def solve_puzzle(request: SolveRequest):
    """Solve a Sudoku puzzle."""
    try:
        grid = request.grid
        
        # Validate grid format
        if len(grid) != 9:
            return SolveResponse(solved=False, error="Grid must have 9 rows")
        
        for row in grid:
            if len(row) != 9:
                return SolveResponse(solved=False, error="Each row must have 9 columns")
            for cell in row:
                if not isinstance(cell, int) or cell < 0 or cell > 9:
                    return SolveResponse(solved=False, error="Cells must be integers 0-9")
        
        solver = SudokuSolver(grid)
        
        # Check if grid is valid
        if not solver.is_valid_grid():
            return SolveResponse(solved=False, error="Invalid grid: contains conflicts")
        
        # Solve
        solution = solver.get_solution()
        
        if solution:
            return SolveResponse(solved=True, solution=solution)
        else:
            return SolveResponse(solved=False, error="Puzzle is unsolvable")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving puzzle: {str(e)}")


@app.post("/api/ocr/", response_model=SolveRequest)
def process_image(file: UploadFile = File(...)):
    """Process uploaded image and extract Sudoku grid."""
    try:
        # Read image bytes
        image_bytes = file.file.read()
        
        # Process with OCR
        ocr = SudokuOCR()
        grid = ocr.process_image_bytes(image_bytes)
        
        if grid is None:
            raise HTTPException(status_code=400, detail="Failed to extract grid from image")
        
        return SolveRequest(grid=grid)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
