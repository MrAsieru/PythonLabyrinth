from tkinter import *
from tkinter import ttk
import random as rnd
from time import sleep

# i\j 1 2 3 4 5
# 1   a b c d e      [[a,b,c,d,e],
# 2   f g h i j      [f,g,h,i,j],
# 3   k l m n o  --> [k,l,m,n,o],  -->  matrix[i][j]
# 4   p q r s t      [p,q,r,s,t],
# 5   u v w x y      [u,v,w,x,y]]
#

#Class for each cell
class Cell(Button):
    i = 0
    j = 0
    state = 0 #0: White 1: Black 2:Start 3:End 4:Path 5:Calculating
    def __init__(self, master, i, j,**kwargs):
        super().__init__(master,**kwargs)
        self.i = i
        self.j = j
        self.state = 0
        super().config(command=self.changeToNextState,bg='white')

    def changeToNextState(self,*args):
        if(self.state == 0):
            super().config(bg='black')
            self.state = 1
        elif(self.state == 1):
            super().config(bg='green')
            self.state = 2
        elif(self.state == 2):
            super().config(bg='red')
            self.state = 3
        elif(self.state == 3):
            super().config(bg='white')
            self.state = 0
            
    def changeState(self,newState,*args):
        if(newState == 0):
            super().config(bg='white')
            self.state = 0
        elif(newState == 1):
            super().config(bg='black')
            self.state = 1
        elif(newState == 2):
            super().config(bg='green')
            self.state = 2
        elif(newState == 3):
            super().config(bg='red')
            self.state = 3
        elif(newState == 4):
            super().config(bg='blue')
            self.state = 4
        elif(newState == 5):
            super().config(bg='yellow')
            self.state = 5

#Class for dijsktra tags
class Tag:
    self_c = "" #i-j
    from_c = "" #i-j
    dist = 0 #Infinity -> -1

    def __init__(self,self_c,from_c,dist):
        self.self_c = self_c
        self.from_c = from_c
        self.dist = dist


#Randomize
def random(*args):
    global cell_matrix
    clear()
    for i in range(len(cell_matrix)):
        for j in range(len(cell_matrix[i])):
            btn = cell_matrix[i][j]
            res = rnd.randint(1,3)
            if res == 1:
                btn.changeState(1)

def clear(*args):
    global cell_matrix
    for i in cell_matrix:
        for j in i:
            j.changeState(0)

def start(*args):
    global cell_matrix, col_num, row_num
    strQ = 0
    endQ = 0
    strCell = None
    endCell = None
    for i in range(row_num):
        for j in range(col_num):
            cell = cell_matrix[i][j]
            if cell.state == 2: #Start
                strQ += 1
                strCell = cell
            elif cell.state == 3: #End
                endQ += 1
                endCell = cell
    if strQ == 0: raise Exception("There is no start point!")
    if strQ > 1: raise Exception("Threre are more than one start point!")
    if endQ == 0: raise Exception("There is no end point!")
    if endQ > 1: raise Exception("Threr are more than one end point!")

    print("Starting...")
    startDijkstra(strCell,endCell)

def startDijkstra(start,end):
    global cell_matrix, col_num, row_num
    
    tag_matrix = []
    #For each cell create a tag
    for i in range(row_num):
        r = []
        for j in range(col_num):
            tag = Tag(str(i)+"-"+str(j),"",-1)
            r.append(tag)
        tag_matrix.append(r)

    #Set start tag dist to zero
    tag_matrix[start.i][start.j].dist = 0
    
    done_array = [tag_matrix[start.i][start.j]]
    tags = dijkstra(tag_matrix[start.i][start.j],tag_matrix[end.i][end.j],tag_matrix,done_array)



    for a in range(row_num):
        for b in range(col_num):
            print(str(tags[a][b].dist)+"\t",end="")
        print("")

    showPath(tag_matrix,tag_matrix[start.i][start.j],tag_matrix[end.i][end.j])

def dijkstra(start,end,tag_matrix,done_array):
    print("Iteration")
    global cell_matrix,col_num, row_num

    #Set usable matrix
    usable_matrix = []
    for a in tag_matrix:
        for b in a:
            if (b.self_c != start.self_c and not(b in done_array) and cell_matrix[int(b.self_c.split("-")[0])][int(b.self_c.split("-")[1])].state != 1):#If cell is not a wall
                usable_matrix.append(b)
    #Check if no usable tags
    if len(usable_matrix) == 0:
        return tag_matrix
    
    #Update tag value (if necessary)
    for a in usable_matrix:
        #Set v1
        v1 = a.dist
        #Set v2
        if (((start.self_c.split("-")[0] == a.self_c.split("-")[0]) and (abs(int(start.self_c.split("-")[1])-int(a.self_c.split("-")[1])) == 1)) or ((start.self_c.split("-")[1] == a.self_c.split("-")[1]) and (abs(int(start.self_c.split("-")[0])-int(a.self_c.split("-")[0])) == 1))):
            v2 = start.dist+1
            print("Start: %s A: %s Dist: %s"%(start.self_c,a.self_c,v2))
            cell_matrix[int(start.self_c.split("-")[0])][int(start.self_c.split("-")[1])].changeState(5)
        else:
            v2 = -1
        #Check min value
        if (v1 == -1 and v2 != -1):                
            if a.dist == -1 or v2 < a.dist:
                a.dist = v2
                a.from_c = start.self_c
        elif (v1 != -1 and v2 == -1):
            if a.dist == -1 or v1 < a.dist:
                a.dist = v1
                a.from_c = start.self_c
        elif (v1 < v2):
            if a.dist == -1 or v1 < a.dist:
                a.dist = v1
                a.from_c = start.self_c
        elif (v2 < v1):
            if a.dist == -1 or v2 < a.dist:
                a.dist = v2
                a.from_c = start.self_c
            
    #Find min tag
    min_tag = usable_matrix[0]
    min_dist = usable_matrix[0].dist
    for a in usable_matrix:
        if min_dist == -1 and a.dist >= 0:
            min_dist = a.dist
            min_tag = a
        
        if a.dist != -1 and a.dist < min_dist:
            min_dist = a.dist
            min_tag = a

    #If no min tag found: No available route
    if min_dist == -1:
        print(done_array)
        for a in usable_matrix:
            print("Self: %s From: %s Dist: %s"%(a.self_c,a.from_c,a.dist))
        raise Exception("No available route")

    #If min tag found check if end
    if min_tag == end:
        return tag_matrix
    else:
        print("Used tag: "+min_tag.self_c)
        done_array.append(min_tag)
        sleep(0.001)
        return dijkstra(min_tag,end,tag_matrix,done_array)

def showPath(tag_matrix,start,end):
    global cell_matrix
    finished = False
    next_tag = None
    current_tag = end
    while not finished:
        next_i = int(current_tag.from_c.split("-")[0])
        next_j = int(current_tag.from_c.split("-")[1])
        next_tag = tag_matrix[next_i][next_j]
        #Print tag info
        print("TAG: %s FROM: %s"%(current_tag.self_c,current_tag.from_c))
        if next_tag == start:
            finished = True
        else:
            #Change cell color with i,j
            cell_matrix[next_i][next_j].changeState(4)
            current_tag = next_tag
        
#Initialize
root = Tk()
root.title("Labyrinth solver") #Set window name

mainframe = ttk.Frame(root,padding="10 10 10 10") #Create the main frame
mainframe.grid(column=0, row=0) #Set it in the first position
labframe = ttk.Frame(mainframe, padding="0 0 0 0") #Create the labirinth frame
labframe.grid(column=0, row=0) #Set it in the first position
btnframe = ttk.Frame(mainframe, padding="0 0 0 0") #Create the btnframe frame
btnframe.grid(column=0, row=1) #Set it in the second position

col_num = 35 #Column length
row_num = 35 #Row length
btn_size = 1 #Size for each button
cell_matrix = [] #Matrix for all cells
print(cell_matrix) #Print the matrix in the console
for i in range(row_num):
    r = []
    for j in range(col_num):
        btn = Cell(labframe,i,j,command=Cell)
        btn.config(height=btn_size,width=2*btn_size)
        btn.grid(column=j,row=i) #Set the button in place
        r.append(btn) #Add the button to the matrix
    cell_matrix.append(r) #Add the row to the matrix

btnClear = Button(btnframe,text="Clear",command=clear)
btnClear.grid(column=0,row=0)

btnRandom = Button(btnframe, text="RANDOMIZE", command=random)
btnRandom.grid(column=1,row=0)

btnStart = Button(btnframe,text="Start", command=start)
btnStart.grid(column=2,row=0)

root.mainloop()#Must be at the end


        
