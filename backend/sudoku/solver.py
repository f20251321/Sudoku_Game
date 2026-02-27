"""
Sudoku solver using backtracking with constraint propagation and MRV heuristic.
"""
from typing import Optional, List, Tuple
import copy


class SudokuSolver:
    """Solves Sudoku puzzles using backtracking with optimization techniques."""
    
    def __init__(self, grid: List[List[int]]):
        """
        Initialize solver with a 9x9 grid.
        Grid should be a list of 9 lists, each containing 9 integers (0-9, 0 = empty).
        """
        self.grid = copy.deepcopy(grid)
        self.solutions = []
        self.max_solutions = 2  # Stop after finding 2 solutions
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        for c in range(9):
            if self.grid[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if self.grid[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] == num:
                    return False
        
        return True
    
    def get_candidates(self, row: int, col: int) -> List[int]:
        """Get valid candidates for a cell using constraint propagation."""
        candidates = []
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                candidates.append(num)
        return candidates
    
    def find_mrv_cell(self) -> Optional[Tuple[int, int]]:
        """
        Find cell with Minimum Remaining Values (MRV) heuristic.
        Returns (row, col) of cell with fewest candidates, or None if grid is complete.
        """
        min_candidates = 10
        best_cell = None
        
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    candidates = self.get_candidates(row, col)
                    if len(candidates) == 0:
                        return None  # Invalid state
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        best_cell = (row, col)
        
        return best_cell
    
    def solve(self, find_all: bool = False) -> bool:
        """
        Solve the Sudoku puzzle using backtracking.
        Returns True if solution found, False otherwise.
        If find_all=True, finds all solutions (up to max_solutions).
        """
        cell = self.find_mrv_cell()
        
        if cell is None:
            # Grid is complete
            if find_all:
                self.solutions.append(copy.deepcopy(self.grid))
                return len(self.solutions) >= self.max_solutions
            return True
        
        row, col = cell
        candidates = self.get_candidates(row, col)
        
        # Try each candidate
        for num in candidates:
            self.grid[row][col] = num
            
            if self.solve(find_all):
                if not find_all:
                    return True
                if len(self.solutions) >= self.max_solutions:
                    return True
            
            # Backtrack
            self.grid[row][col] = 0
        
        return False
    
    def get_solution(self) -> Optional[List[List[int]]]:
        """Get the solved grid. Returns None if unsolvable."""
        if self.solve():
            return self.grid
        return None
    
    def count_solutions(self) -> int:
        """Count the number of solutions (up to max_solutions)."""
        self.solutions = []
        self.solve(find_all=True)
        return len(self.solutions)
    
    def is_valid_grid(self) -> bool:
        """Check if the initial grid is valid (no conflicts)."""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    num = self.grid[row][col]
                    self.grid[row][col] = 0
                    if not self.is_valid(row, col, num):
                        self.grid[row][col] = num
                        return False
                    self.grid[row][col] = num
        return True
