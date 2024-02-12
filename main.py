import tkinter as tk
import random
from queue import PriorityQueue, Queue

class PathFindingGame:
    def __init__(self, rows, columns, cell_size):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]
        self.rat_location = None
        self.cheese_location = None
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, 1, -1]
        self.vis = [[None for _ in range(columns)] for _ in range(rows)]
        self.obstacle_prob = 0.3  # Probability of a cell being an obstacle
        self.delay = 0  # Delay in milliseconds
        self.path_delay = 20  # Delay between cells in path visualization
        self.ok=False
        self.wall_color="darkgreen"
        self.roads_color="lightgreen"
        self.path_color="olive"
        

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                # if self.ok is False:
                if random.random() < self.obstacle_prob:
                    color = self.wall_color  # Cell is an obstacle
                else:
                    color = "white"  # Cell is open
                # else:
                #     if self.grid[i][j]["bg"] =="brown":
                #         color="brown"
                #     else:
                #         color="white"
                # self.grid[i][j]=None
                # self.tempgrid[i][j]=None
                cell = tk.Canvas(root, width=self.cell_size, height=self.cell_size, bg=color, bd=1)
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", lambda event, row=i, col=j: self.cell_click(event, row, col))
                self.grid[i][j] = cell
                self.vis[i][j] = None
        self.ok=True
    def cell_click(self, event, row, col):
        if self.rat_location is None:
            self.grid[row][col].config(bg="gray")
            self.rat_location = (row, col)
        elif self.cheese_location is None:
            self.grid[row][col].config(bg="gray")
            self.cheese_location = (row, col)

    def update_color_with_delay(self, point, color, delay):
        row, col = point
        if self.grid[row][col]["bg"]!="gray":
            self.grid[row][col].after(delay, lambda: self.grid[row][col].config(bg=color))
    def h1(self,curr):
        return abs(curr[0] - self.cheese_location[0]) + abs(curr[1] - self.cheese_location[1])  
    # BBBBBBBBBBBBBBBBBBFFFFFFFFFFFFFFFFFFFFFFFFFSSSSSSSSSSSSSSSSSSSSSSSSS
    def bfs(self):
        queue = Queue()
        queue.put(self.rat_location)

        while not queue.empty():
            current = queue.get()
            if current == self.cheese_location:
                path = []
                temp = current
                while temp != self.rat_location:
                    path.append(temp)
                    temp = self.vis[temp[0]][temp[1]]
                path.pop(0)
                path.reverse()

                # Update the path with delay between cells
                delay = self.path_delay
                for point in path:
                    self.update_color_with_delay(point, self.path_color, delay)
                    delay += self.path_delay

                return path

            for i in range(4):
                new_x = current[0] + self.dx[i]
                new_y = current[1] + self.dy[i]

                if 0 <= new_x < self.rows and 0 <= new_y < self.columns and \
                        self.grid[new_x][new_y]["bg"] !=  self.wall_color and self.vis[new_x][new_y] is None:
                    self.vis[new_x][new_y] = current
                    queue.put((new_x, new_y))
                    if self.grid[new_x][new_y]["bg"]!="gray":
                        self.update_color_with_delay((new_x, new_y),  self.roads_color, 0)  # Change color to indicate exploration

        return []
    # DDDDDDDDDDDDDDDDDDFFFFFFFFFFFFFFFFFFFFFFFFFSSSSSSSSSSSSSSSSSSSSSSSSS
    def dfs(self,curr_x,curr_y):
        self.vis[curr_x][curr_y]=(curr_x,curr_y)
        path=[(curr_x,curr_y)]
        if (curr_x,curr_y) == self.cheese_location:
            return path
        
        for i in range(4):
                new_x = curr_x + self.dx[i]
                new_y = curr_y + self.dy[i]

                if 0 <= new_x < self.rows and 0 <= new_y < self.columns and \
                        self.grid[new_x][new_y]["bg"] != self.wall_color and self.vis[new_x][new_y] is None:
                    self.vis[new_x][new_y] = (curr_x,curr_y)
                    if self.grid[new_x][new_y]["bg"]!="gray":                    
                        self.update_color_with_delay((new_x, new_y),  self.roads_color, 0)   # Change color to indicate exploration
                    ppath=game.dfs(new_x,new_y)
                    if len(ppath)!=0:
                        return path+ppath
        return []
    # GGGGGGGGGGGGGGRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEDDDDDDDDDYYYYYYYYY
    def greedy_best_first(self):
        queue = PriorityQueue()
        queue.put((0, self.rat_location))  # Initialize with the rat's location and priority 0
        while not queue.empty():
            _, current = queue.get()  # Discard the priority, just need the node location
            if current == self.cheese_location:
                path = []
                temp = current
                while temp != self.rat_location:
                    path.append(temp)
                    temp = self.vis[temp[0]][temp[1]]
                path.pop(0)
                path.reverse()

                # Update the path with delay between cells
                delay = self.path_delay
                for point in path:
                    self.update_color_with_delay(point, self.path_color, delay)
                    delay += self.path_delay

                return path

            for i in range(4):
                new_x = current[0] + self.dx[i]
                new_y = current[1] + self.dy[i]

                if 0 <= new_x < self.rows and 0 <= new_y < self.columns and \
                        self.grid[new_x][new_y]["bg"] != self.wall_color and self.vis[new_x][new_y] is None:
                    self.vis[new_x][new_y] = current
                    # Calculate heuristic cost (Manhattan distance in this case)
                    heuristic_cost = self.h1((new_x,new_y))
                    queue.put((heuristic_cost, (new_x, new_y)))  # Priority based on heuristic cost
                    if self.grid[new_x][new_y]["bg"]!="gray":                    
                     self.update_color_with_delay((new_x, new_y),  self.roads_color, 0)   # Change color to indicate exploration
        return []
    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    def A_star(self):
        start = self.rat_location
        goal = self.cheese_location

        # Priority queue for A* algorithm
        frontier = PriorityQueue()
        frontier.put((0, start))
        
        # Cost to reach each node
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                path = []
                temp = current
                while temp != start:
                    path.append(temp)
                    temp = self.vis[temp[0]][temp[1]]
                path.reverse()

                # Update the path with delay between cells
                delay = self.path_delay
                for point in path:
                    self.update_color_with_delay(point, self.path_color, delay)
                    delay += self.path_delay

                return path

            for i in range(4):
                new_x = current[0] + self.dx[i]
                new_y = current[1] + self.dy[i]

                if 0 <= new_x < self.rows and 0 <= new_y < self.columns and \
                        self.grid[new_x][new_y]["bg"] != self.wall_color:
                            
                    new_cost = cost_so_far[current] + 1
                    if (new_x, new_y) not in cost_so_far or new_cost < cost_so_far[(new_x, new_y)]:
                        
                        cost_so_far[(new_x, new_y)] = new_cost
                        priority = new_cost + self.h1((new_x, new_y))
                        frontier.put((priority, (new_x, new_y)))
                        self.vis[new_x][new_y] = current
                        self.update_color_with_delay((new_x, new_y), self.roads_color, 0)

        return []
    #limiteddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    def dfs_limited(self,curr_x,curr_y,curr_len,limit):
        self.vis[curr_x][curr_y]=limit
        path=[(curr_x,curr_y)]
        if (curr_x,curr_y) == self.cheese_location:
            return path
        
        for i in range(4):
                new_x = curr_x + self.dx[i]
                new_y = curr_y + self.dy[i]

                if 0 <= new_x < self.rows and 0 <= new_y < self.columns and \
                        self.grid[new_x][new_y]["bg"] != self.wall_color and self.vis[new_x][new_y] != limit  and curr_len!=limit:
                    self.vis[new_x][new_y] = (curr_x,curr_y)
                    if self.grid[new_x][new_y]["bg"]!="gray":                    
                        self.update_color_with_delay((new_x, new_y),  self.roads_color, 0)  # Change color to indicate exploration
                    ppath=game.dfs_limited(new_x,new_y,curr_len+1,limit)
                    if len(ppath)!=0:
                        return path+ppath
        return []
        
    def find_bfs(self):
        if self.rat_location is None or self.cheese_location is None:
            tk.messagebox.showinfo("Error", "Please place the rat and the cheese before finding a path.")
            return

        path = self.bfs()
        if not path:
            tk.messagebox.showinfo("No Path", "No path found.")
    def find_greedy(self):
        if self.rat_location is None or self.cheese_location is None:
            tk.messagebox.showinfo("Error", "Please place the rat and the cheese before finding a path.")
            return

        path = self.greedy_best_first()
        if not path:
            tk.messagebox.showinfo("No Path", "No path found.")        
    def find_dfs(self):
        if self.rat_location is None or self.cheese_location is None:
            tk.messagebox.showinfo("Error", "Please place the rat and the cheese before finding a path.")
            return

        path = self.dfs(self.rat_location[0],self.rat_location[1])
        for point in path:
            self.update_color_with_delay(point, self.path_color, self.delay)
            self.delay += self.path_delay
        
        

        if not path:
            tk.messagebox.showinfo("No Path", "No path found.")
    def find_A(self):
        if self.rat_location is None or self.cheese_location is None:
            tk.messagebox.showinfo("Error", "Please place the rat and the cheese before finding a path.")
            return  

        path = self.A_star()
        # for point in path:
        #     self.update_color_with_delay(point, self.path_color, self.delay)
        #     self.delay += self.path_delay

        if not path:
            tk.messagebox.showinfo("No Path", "No path found.")

    def find_dfs_limited(self):
        if self.rat_location is None or self.cheese_location is None:
            tk.messagebox.showinfo("Error", "Please place the rat and the cheese before finding a path.")
            return
        l =2
        while l < 10000:  
            path = self.dfs_limited(self.rat_location[0], self.rat_location[1], 0, l)
            if path: 
                for point in path:
                    self.update_color_with_delay(point,self.path_color, self.delay)
                    self.delay += self.path_delay 
                break
            l *= 2        
        if not path:
            tk.messagebox.showinfo("No Path", "No path found.")
    
    def reset(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j]["bg"]!= self.wall_color:
                    self.update_color_with_delay((i,j), "white", 0)

                self.vis[i][j]=None



# Create the main window
root = tk.Tk()
root.title("Path-Finding Game")

game = PathFindingGame(rows=30, columns=40, cell_size=15)
game.create_grid()

find_path_button = tk.Button(root, text="bridth-fs", command=game.find_bfs)
find_path_button.grid(row=game.rows, column=0, columnspan=game.columns, pady=10)

find_path_button = tk.Button(root, text="depth-fs", command=game.find_dfs)
find_path_button.grid(row=game.rows, column=6, columnspan=game.columns, pady=10)

find_path_button = tk.Button(root, text="greedy-bs", command=game.find_greedy)
find_path_button.grid(row=game.rows, column=12, columnspan=game.columns, pady=10)

find_path_button = tk.Button(root, text="A*", command=game.find_A)
find_path_button.grid(row=game.rows, column=17, columnspan=game.columns, pady=10)

find_path_button = tk.Button(root, text="limited-dfs", command=game.find_dfs_limited)
find_path_button.grid(row=game.rows, column=22, columnspan=game.columns, pady=10)

find_path_button = tk.Button(root, text="Reset", command=game.reset)
find_path_button.grid(row=game.rows, column=29, columnspan=game.columns, pady=10)

root.mainloop()