"""
Sudoku puzzle generator with difficulty levels.
"""
import random
from typing import List, Tuple
from .solver import SudokuSolver


class SudokuGenerator:
    """Generates valid Sudoku puzzles with exactly one solution."""
    
    # Difficulty settings: (min_clues, max_clues, recursion_depth_threshold)
    DIFFICULTY_SETTINGS = {
        'easy': (36, 46, 5),
        'medium': (28, 35, 10),
        'hard': (22, 27, 20),
        'expert': (17, 21, 50)
    }
    
    def __init__(self):
        self.solver = None
    
    def generate_complete_grid(self) -> List[List[int]]:
        """Generate a complete, valid Sudoku grid."""
        grid = [[0] * 9 for _ in range(9)]
        self._fill_grid(grid)
        return grid
    
    def _fill_grid(self, grid: List[List[int]]) -> bool:
        """Recursively fill grid using backtracking."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self._is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self._fill_grid(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    
    def _is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        for c in range(9):
            if grid[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if grid[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == num:
                    return False
        
        return True
    
    def _remove_cells(self, grid: List[List[int]], num_to_remove: int) -> List[List[int]]:
        """Remove cells while ensuring unique solution."""
        puzzle = [row[:] for row in grid]
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= num_to_remove:
                break
            
            # Try removing this cell
            original = puzzle[row][col]
            puzzle[row][col] = 0
            
            # Check if still has unique solution
            solver = SudokuSolver(puzzle)
            if solver.is_valid_grid():
                solution_count = solver.count_solutions()
                if solution_count == 1:
                    removed += 1
                else:
                    # Restore if multiple solutions
                    puzzle[row][col] = original
            else:
                puzzle[row][col] = original
        
        return puzzle
    
    def generate(self, difficulty: str = 'medium') -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate a Sudoku puzzle with specified difficulty.
        Returns (puzzle, solution) tuple.
        """
        if difficulty not in self.DIFFICULTY_SETTINGS:
            difficulty = 'medium'
        
        min_clues, max_clues, _ = self.DIFFICULTY_SETTINGS[difficulty]
        target_clues = random.randint(min_clues, max_clues)
        num_to_remove = 81 - target_clues
        
        # Generate complete grid
        solution = self.generate_complete_grid()
        
        # Remove cells to create puzzle
        puzzle = self._remove_cells(solution, num_to_remove)
        
        # Verify unique solution
        solver = SudokuSolver(puzzle)
        solution_count = solver.count_solutions()
        
        # If not unique, try again (with slightly more clues)
        attempts = 0
        while solution_count != 1 and attempts < 10:
            if solution_count == 0:
                # Invalid puzzle, regenerate
                solution = self.generate_complete_grid()
                puzzle = self._remove_cells(solution, num_to_remove)
            else:
                # Multiple solutions, add a clue back
                empty_cells = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
                if empty_cells:
                    row, col = random.choice(empty_cells)
                    puzzle[row][col] = solution[row][col]
            
            solver = SudokuSolver(puzzle)
            solution_count = solver.count_solutions()
            attempts += 1
        
        if solution_count != 1:
            # Fallback: return puzzle with more clues
            puzzle = self._remove_cells(solution, 81 - max_clues)
        
        return puzzle, solution
