# Sudoku Arena

A full-stack web application for playing and solving Sudoku puzzles with image recognition capabilities.

## Features

### Play Sudoku
- Generate puzzles with 4 difficulty levels: Easy, Medium, Hard, Expert
- Automatic timer that starts when puzzle loads
- Real-time validation when puzzle is completed
- Keyboard navigation support

### Solve Sudoku
- Manual input mode: Enter puzzle grid manually
- Image upload mode: Upload an image of a Sudoku puzzle
  - Automatic grid detection and cell extraction
  - OCR using Tesseract for digit recognition
- Backend solver with backtracking algorithm

## Tech Stack

- **Backend**: Python (FastAPI)
- **Frontend**: React (Vite)
- **OCR**: OpenCV + Tesseract
- **Solver**: Backtracking with constraint propagation and MRV heuristic

## Project Structure

```
sudoku/
├── backend/
│   ├── sudoku/
│   │   ├── __init__.py
│   │   ├── solver.py          # Sudoku solver with backtracking
│   │   └── generator.py       # Puzzle generator with difficulty levels
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── image_processor.py # Image processing and OCR
│   ├── api/
│   │   └── main.py            # FastAPI application and endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── PlaySudoku.jsx
│   │   │   ├── SolveSudoku.jsx
│   │   │   ├── SudokuBoard.jsx
│   │   │   └── Timer.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed
3. **Tesseract OCR** installed:
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
python run_server.py
```

Or using uvicorn directly:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: Make sure you're in the `backend` directory when running the server.

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### `POST /api/generate/`
Generate a new Sudoku puzzle.

**Request:**
```json
{
  "difficulty": "easy" | "medium" | "hard" | "expert"
}
```

**Response:**
```json
{
  "puzzle": [[...], ...],  // 9x9 grid with 0 for empty cells
  "solution": [[...], ...] // 9x9 complete solution
}
```

### `POST /api/solve/`
Solve a Sudoku puzzle.

**Request:**
```json
{
  "grid": [[...], ...]  // 9x9 grid with 0 for empty cells
}
```

**Response:**
```json
{
  "solved": true,
  "solution": [[...], ...]  // 9x9 solved grid
}
```

Or if unsolvable:
```json
{
  "solved": false,
  "error": "Error message"
}
```

### `POST /api/ocr/`
Extract Sudoku grid from uploaded image.

**Request:**
- Multipart form data with `file` field containing image

**Response:**
```json
{
  "grid": [[...], ...]  // 9x9 grid extracted from image
}
```

## Solver Algorithm

The solver uses:
- **Backtracking**: Recursive search with backtracking
- **Constraint Propagation**: Prunes invalid candidates early
- **MRV Heuristic**: Minimum Remaining Values - selects cells with fewest candidates first
- **Solution Counting**: Can detect no solution or multiple solutions

## Generator Algorithm

The generator:
1. Creates a complete, valid Sudoku grid
2. Removes cells while ensuring unique solution
3. Adjusts clue count based on difficulty:
   - Easy: 36-46 clues
   - Medium: 28-35 clues
   - Hard: 22-27 clues
   - Expert: 17-21 clues

## OCR Process

1. **Preprocessing**: Grayscale conversion, Gaussian blur, adaptive thresholding
2. **Grid Detection**: Contour detection, perspective transform
3. **Cell Extraction**: Split 450x450 grid into 81 cells (9x9)
4. **Digit Recognition**: Tesseract OCR on each cell

## Development Notes

- The solver is optimized for correctness and efficiency
- The generator ensures exactly one solution for each puzzle
- OCR accuracy depends on image quality - clear, well-lit images work best
- Frontend uses React Router for navigation
- Timer automatically starts when puzzle loads in Play mode

## Troubleshooting

### OCR not working
- Ensure Tesseract is installed and in PATH
- Try with clearer, higher resolution images
- Ensure good lighting and contrast in the image

### CORS errors
- Make sure backend CORS settings include your frontend URL
- Check that both servers are running

### Import errors
- Ensure you're running from the correct directory
- Check that all Python dependencies are installed
- Verify virtual environment is activated

## License

This project is open source and available for educational purposes.
