"""
Image processing and OCR for Sudoku puzzles.
"""
import cv2
import numpy as np
from typing import List, Optional, Tuple
import pytesseract
from PIL import Image


class SudokuOCR:
    """Processes images of Sudoku puzzles and extracts the grid."""
    
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image: grayscale, thresholding, deskew."""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        return thresh
    
    def find_grid(self, image: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """Find the Sudoku grid in the image."""
        # Find contours
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find largest contour (should be the grid)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Approximate contour to polygon
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        if len(approx) != 4:
            # Try to find rectangular shape
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            approx = np.int0(box)
        
        # Get corners
        corners = self._order_points(approx.reshape(-1, 2))
        
        # Perspective transform
        width = 450
        height = 450
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype='float32')
        
        M = cv2.getPerspectiveTransform(corners.astype('float32'), dst)
        warped = cv2.warpPerspective(image, M, (width, height))
        
        return warped, M
    
    def _order_points(self, pts: np.ndarray) -> np.ndarray:
        """Order points: top-left, top-right, bottom-right, bottom-left."""
        rect = np.zeros((4, 2), dtype='float32')
        
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left
        rect[2] = pts[np.argmax(s)]  # bottom-right
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right
        rect[3] = pts[np.argmax(diff)]  # bottom-left
        
        return rect
    
    def split_into_cells(self, grid_image: np.ndarray) -> List[List[np.ndarray]]:
        """Split 450x450 grid image into 81 cells (9x9)."""
        cells = []
        cell_size = 50  # 450 / 9
        
        for row in range(9):
            cell_row = []
            for col in range(9):
                y1 = int(row * cell_size)
                y2 = int((row + 1) * cell_size)
                x1 = int(col * cell_size)
                x2 = int((col + 1) * cell_size)
                
                cell = grid_image[y1:y2, x1:x2]
                # Add padding
                cell = cv2.copyMakeBorder(cell, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255)
                cell_row.append(cell)
            cells.append(cell_row)
        
        return cells
    
    def recognize_digit(self, cell_image: np.ndarray) -> int:
        """Recognize digit in a cell using Tesseract OCR."""
        # Invert for Tesseract (expects dark text on light background)
        cell_inv = cv2.bitwise_not(cell_image)
        
        # Resize for better OCR
        cell_resized = cv2.resize(cell_inv, (50, 50), interpolation=cv2.INTER_CUBIC)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(cell_resized)
        
        try:
            text = pytesseract.image_to_string(pil_image, config=self.tesseract_config).strip()
            if text and text.isdigit() and 1 <= int(text) <= 9:
                return int(text)
        except Exception:
            pass
        
        return 0
    
    def process_image(self, image_path: str) -> Optional[List[List[int]]]:
        """
        Process image and extract Sudoku grid.
        Returns 9x9 grid (0 for empty cells) or None if failed.
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Preprocess
            processed = self.preprocess_image(image)
            
            # Find grid
            result = self.find_grid(processed)
            if result is None:
                return None
            
            grid_image, _ = result
            
            # Split into cells
            cells = self.split_into_cells(grid_image)
            
            # OCR each cell
            grid = []
            for row in range(9):
                grid_row = []
                for col in range(9):
                    digit = self.recognize_digit(cells[row][col])
                    grid_row.append(digit)
                grid.append(grid_row)
            
            return grid
        
        except Exception as e:
            print(f"OCR Error: {e}")
            return None
    
    def process_image_bytes(self, image_bytes: bytes) -> Optional[List[List[int]]]:
        """Process image from bytes (for API upload)."""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return None
            
            # Preprocess
            processed = self.preprocess_image(image)
            
            # Find grid
            result = self.find_grid(processed)
            if result is None:
                return None
            
            grid_image, _ = result
            
            # Split into cells
            cells = self.split_into_cells(grid_image)
            
            # OCR each cell
            grid = []
            for row in range(9):
                grid_row = []
                for col in range(9):
                    digit = self.recognize_digit(cells[row][col])
                    grid_row.append(digit)
                grid.append(grid_row)
            
            return grid
        
        except Exception as e:
            print(f"OCR Error: {e}")
            return None
