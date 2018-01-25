import Tkinter as tk
import math
import PriorityQueue as pq
import Output as ot
import Control as cl
import time

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0,column=0)
        self.rows = 10
        self.columns = 10
        self.startNode=[]
        self.goalNode=[]
        self.wallNode=[]
        self.tiles = {}
        self.canvas.bind("<Configure>", self.draw_grid)
        #control Canvas
        self.control=cl.Control(self)
        self.control.grid(row=0, column=2)
        self.control.runButton.configure(command=self.run)
        self.control.clearButton.configure(command=self.clear)
        self.control.quitButton.configure(command=self.quit)
        #output canvas
        self.output=ot.Output(self)
        self.output.grid(row=2,column=0)

    def quit(self):
        self.canvas.quit()

    def clear(self):
        for row in range(self.rows):
            for col in range(self.columns):
                tile = self.tiles[row, col]
                tile_color = self.canvas.itemcget(tile, "fill")
                new_color = "white" if tile_color != "white" else "white"
                self.canvas.itemconfigure(tile, fill=new_color)

    def walls(self):
        wall=[]
        for row in range(self.rows):
            for col in range(self.columns):
                tile = self.tiles[row, col]
                tile_color = self.canvas.itemcget(tile, "fill")
                if tile_color=="black":
                    node=[row,col]
                    wall.append(node)
        return wall

    def draw_grid(self, event=None):
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.rows)
        for column in range(self.columns):
            for row in range(self.rows):
                tile = self.canvas.create_rectangle(column*cellwidth, row * cellheight,
                                                    column * cellwidth + cellwidth, row * cellheight + cellheight,
                                                    fill="white", tags="rect")
                self.tiles[row,column] = tile
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row, column=column: self.cell_clicked(row, column))

    def cell_clicked(self, row, column):
        tile = self.tiles[row, column]
        tile_color = self.canvas.itemcget(tile, "fill")
        if self.control.var.get() == "start":
            new_color = "red" if tile_color == "white" else "white"
            self.startNode=[row,column]
        elif self.control.var.get()=="goal":
            new_color = "green" if tile_color == "white" else "white"
            self.goalNode = [row, column]
        elif self.control.var.get()=="wall":
            new_color = "black" if tile_color == "white" else "white"
            self.wallNode = [row, column]
        self.canvas.itemconfigure(tile, fill=new_color)

    def heuristic_manhatten(self,start,goal):
        result=0
        try:
            result=abs(start[0] - goal[0])+abs(start[1] - goal[1])
        except IndexError:
            self.output.result.configure(text="Place start and goal!!", bg="red")
        return result

    def heuristic_euclidean(self,start,goal):
        dx=0
        dy=0
        try:
            dx = abs(start[0] - goal[0])
            dy = abs(start[1] - goal[1])
        except IndexError:
            self.output.result.configure(text="Place start and goal!!", bg="red")
        return math.sqrt(dx*dx+dy*dy)

    def colour_parent(self,row,column):
        tile = self.tiles[row, column]
        tile_color = self.canvas.itemcget(tile, "fill")
        new_color=None
        if tile_color !="red" and tile_color !="green":
            new_color="blue"
        self.canvas.itemconfigure(tile, fill=new_color)

    def colour_openlist(self,row,column):
        tile = self.tiles[row, column]
        tile_color = self.canvas.itemcget(tile, "fill")
        new_color=None
        if tile_color !="blue" and tile_color !="red" and tile_color !="green" and tile_color!="purple":
            new_color="orange"
        self.canvas.itemconfigure(tile, fill=new_color)

    def colour_path(self,row,column):
        tile = self.tiles[row, column]
        tile_color = self.canvas.itemcget(tile, "fill")
        new_color=None
        if tile_color !="red" and tile_color !="green":
            new_color="purple"
        self.canvas.itemconfigure(tile, fill=new_color)

    def cost(self,current):
        x,y=current
        cost=0
        neighbours=self.neighbors(current)
        for neighbour in neighbours:
            x1,y1=neighbour
            if x1==x-1 and y1==y or x1==x and y1==y+1 or x1==x+1 and y1==y or x1==x and y1==y-1:
                g=1
                cost=g
            elif x1==x-1 and y1==y+1 or x1==x+1 and y1==y+1 or x1==x+1 and y1==y-1 or x1==x-1 and y1==y-1:
                g=1.4
                cost=g
        return cost

    def neighbors(self, node):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [+1, -1], [-1, +1]]
        neighbors = []
        for dir in dirs:
            neighbor = [node[0] + dir[0], node[1] + dir[1]]
            if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.columns:
                if neighbor not in self.walls():
                    neighbors.append(neighbor)
        return neighbors

    def a_star_search(self,start,goal):
        start=self.startNode
        goal=self.goalNode
        frontier=pq.PriorityQueue()
        frontier.put(start,0)
        parent=[]
        openlist=[]
        cameFrom={}
        f = 0
        cost=0
        found = False
        while not frontier.empty():
            current=frontier.get()
            parent.append(current)
            if current==goal:
                found=True
                break
            for neighbour in self.neighbors(current):
                #ignore neighbour in closed list
                if neighbour not in parent:
                    #discover new node
                    if neighbour not  in openlist:
                        openlist.append(neighbour)
                        if self.control.var1.get() == "Manhatten":
                            f = self.heuristic_manhatten(neighbour, goal) + self.cost(neighbour)
                        elif self.control.var1.get() == "Euclidean":
                            f = self.heuristic_euclidean(neighbour, goal) + self.cost(neighbour)
                        frontier.put(neighbour,f)
                        cameFrom[tuple(neighbour)]=current
            heuristic=self.heuristic_manhatten(current,goal)
            cost+=self.heuristic_manhatten(current,goal)
            for node in parent:
                self.colour_parent(node[0],node[1])
        if found==True:
            self.output.result.configure(text="Goal Found!!",bg="green")
            self.recontruct_path(cameFrom)
            for open in openlist:
                self.colour_openlist(open[0],open[1])
        else:
            self.output.result.configure(text="No Possible Path!!",bg="red")

    def recontruct_path(self,came_from):
        current=self.goalNode
        try:
            path=[tuple(current)]
            while current!=self.startNode:
                current=came_from[tuple(current)]
                path.append(current)
            for node in path:
                self.colour_path(node[0],node[1])
        except IndexError:
            self.output.result.configure(text="Place start and goal!!", bg="red")

    def run(self):
        start=time.time()
        self.a_star_search(self.startNode,self.goalNode)
        duration=time.time() - start
        self.output.timeValue.configure(text=round(duration,2))