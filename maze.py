from tkinter import Tk, BOTH, Canvas
import time,random
class Window(): #Create a window
    
    def __init__(self,width,height):
        self.root = Tk()
        self.root.title("Welcome to maze solver!")
        self.canvas = Canvas(self.root, bg="white",height = height,width = width)
        self.canvas.pack()
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False

    def draw_line(self,line,fill_color):
        line.draw(self.canvas,fill_color)
        
class Point():
    def __init__(self,x,y):
        self.x = x   
        self.y = y 
    
class Line():
    def __init__(self,p1,p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y
    def draw(self,canvas,fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)
        canvas.pack()

class Cell():
    def __init__(self,win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._visited = False
        self._win = win
        
    
    def draw(self,x1,y1,x2,y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        bottom_right = Point(x2,y2)
        top_right = Point(x2,y1)
        bottom_left = Point(x1,y2)
        top_left = Point(x1,y1)

        if self.has_left_wall:
            line = Line(top_left,bottom_left)
            if self._win != None:
                self._win.draw_line(line,fill_color = "black")
        else:
            line = Line(top_left,bottom_left)
            if self._win != None:
                self._win.draw_line(line,fill_color = "white")
        if self.has_right_wall:
            line = Line(top_right,bottom_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "black")
        else:
            line = Line(top_right,bottom_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "white")
        if self.has_top_wall:
            line = Line(top_left,top_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "black")
        else:
            line = Line(top_left,top_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "white")
        if self.has_bottom_wall:
            line = Line(bottom_left,bottom_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "black")
        else:
            line = Line(bottom_left,bottom_right)
            if self._win != None:
                self._win.draw_line(line,fill_color = "white")

    def draw_move(self, to_cell, undo=False):
        c1 = Point(self._x1 + (self._x2 - self._x1) / 2,self._y1 + (self._y2 - self._y1) / 2)
        c2 = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1) / 2,to_cell._y1 + (to_cell._y2 - to_cell._y1) / 2)
        line = Line(c1,c2)
        if undo:
            self._win.draw_line(line,fill_color = "white")
        else:
            self._win.draw_line(line,fill_color = "red")   
    

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed != None:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = [[Cell(self._win)for j in range(self._num_cols)] for i in range(self._num_rows)]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j) 
    
    def _draw_cell(self,i,j):
        tl_x = self._x1 + self._cell_size_x * i 
        tl_y = self._y1 + self._cell_size_y * j 
        br_x = tl_x + self._cell_size_x
        br_y = tl_y + self._cell_size_y
        self._cells[j][i].draw(tl_x,tl_y,br_x,br_y)
        self._animate()
    
    def _animate(self):
        if self._win != None:
            self._win.redraw()
            time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_rows - 1][self._num_cols - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1,self._num_rows - 1)
        
    def _break_walls_r(self,i,j):
        self._cells[i][j]._visited = True
        loop = True
        while(loop):
            can_visit = []
            top,bottom,left,right = i-1,i+1,j-1,j+1
            if top >= 0:
                if self._cells[top][j]._visited == False:
                    can_visit.append([top,j])
            if bottom < self._num_rows:
                if self._cells[bottom][j]._visited == False:
                    can_visit.append([bottom,j])
            if left >= 0:
                if self._cells[i][left]._visited == False:
                    can_visit.append([i,left])
            if right < self._num_cols:
                if self._cells[i][right]._visited == False:
                    can_visit.append([i,right])
            if len(can_visit) == 0:
                self._draw_cell(j,i)
                loop = False
                return
            choosen_cell = random.choice(can_visit)
            if choosen_cell[1] == left:
                self._cells[i][j].has_left_wall = False
                self._cells[i][left].has_right_wall = False
                self._draw_cell(j,i)
                self._draw_cell(left,i)
            elif choosen_cell[1] == right:
                self._cells[i][j].has_right_wall = False
                self._cells[i][right].has_left_wall = False
                self._draw_cell(j,i)
                self._draw_cell(right,i)
            elif choosen_cell[0] == top:
                self._cells[i][j].has_top_wall = False
                self._cells[top][j].has_bottom_wall = False
                self._draw_cell(j,i)
                self._draw_cell(j,top)
            elif choosen_cell[0] == bottom:
                self._cells[i][j].has_bottom_wall = False
                self._cells[bottom][j].has_top_wall = False
                self._draw_cell(j,i)
                self._draw_cell(j,bottom)
            self._break_walls_r(choosen_cell[0],choosen_cell[1])

    def _reset_cells_visited(self):
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._cells[i][j]._visited = False
                
    def solve(self):
        if self._solve_r(0,0):
            return True
        return False
    
    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j]._visited = True
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True
        directions = []
        if self._cells[i][j].has_top_wall == False:
            directions.append([i-1,j])
        if self._cells[i][j].has_bottom_wall == False:
            directions.append([i+1,j])
        if self._cells[i][j].has_left_wall == False:
            directions.append([i,j-1])
        if self._cells[i][j].has_right_wall == False:
            directions.append([i,j+1]) 
        for dir in directions:
            if dir[0] >= 0 and dir[0] < self._num_rows and dir[1] >= 0 and dir[1] < self._num_cols and self._cells[dir[0]][dir[1]]._visited == False:
                self._cells[i][j].draw_move(self._cells[dir[0]][dir[1]])
                if self._solve_r(dir[0],dir[1]):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[dir[0]][dir[1]],True)
        return False


def main():
    win = Window(800, 600)
    m = Maze(50,50,10,14,50,50,win)
    m._break_entrance_and_exit()
    m._break_walls_r(9,13)
    m._reset_cells_visited()
    m.solve()
    win.wait_for_close()
    
main()  # comment out this main while running tests.py
