import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_cell_visited(self):
        num_cols = 5
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        for i in range(num_rows):
            for j in range(num_cols):
                self.assertEqual(
                    False,
                    m1._cells[i][j]._visited,
                )

    def test_break_entry_and_exit(self):
        num_cols = 9
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 9, 9)
        m1._break_entrance_and_exit()
        self.assertEqual(
            False,
            m1._cells[0][0].has_top_wall,
        )
        self.assertEqual(
            False,
            m1._cells[num_rows-1][num_cols-1].has_bottom_wall,
        )
        
    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 15
        m1 = Maze(0, 0, num_rows, num_cols, 15, 15)
        m1._break_walls_r(num_rows-1,num_cols-1)
        m1._reset_cells_visited()
        for i in range(num_rows):
            for j in range(num_cols):
                self.assertEqual(
                    False,
                    m1._cells[i][j]._visited,
                )

if __name__ == "__main__":
    unittest.main()