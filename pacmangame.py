import random

class Maze:

    def __init__(self,layout , lives = 3):
        self.layout = layout
        self.scores = 0
        self.pacman_position = self.startposition()
        self.ghost_position = self.create_ghost()
        self.lives = lives
        self.power_up = False
        self.power_up_duration = 0

    def startposition(self):
        r = 0
        while(r < len(self.layout)):
            c = 0
            while(c < len(self.layout[r])):
                if(self.layout[r][c] == 0 ):
                    return(r , c)
                c = c + 1
            r = r + 1
        return(0 , 0)

    def create_ghost(self):
        ghost = []
        l = 0
        for y in self.layout:
            for x in y:
                if( x == 0):
                   l = l+1
        if(l > 3):
           l= 3
        for x in range(l):
            while(True):
                r = random.randint(0, len(self.layout) -1 )
                c = random.randint(0 , len(self.layout[r]) - 1)
                if(self.layout[r][c] == 0 and self.pacman_position != self.layout[r][c]):
                   ghost.append((r,c))
                   break
        return ghost

    def move_ghost(self):
        if(self.power_up):
            y = 0
            while(y < len(self.ghost_position)):
                b=self.ghost_position[y]
                a = self.random_ghost_position(b)
                if(a != self.pacman_position):
                   self.ghost_position[y] = a
                y = y + 1

    def random_ghost_position(self , ghost_pos):
        row, col = ghost_pos
        possiblepos = [(row+1,col),(row,col+1),(row-1 , col),(row, col-1)]
        new_pos = filter(self.is_validmove,possiblepos)
        new_pos = list(new_pos)
        return random.choice(list(new_pos) if new_pos else ghost_pos)

    def display(self):
        print()
        print("scores : ",self.scores)
        print("Lives : ", self.lives )
        print("is power up on ", self.power_up)
        print("power up duration : ",self.power_up_duration)
        print()
        r = 0
        while(r < len(self.layout)):
            c = 0
            while(c < len(self.layout[r])):
                if (r, c) == self.pacman_position:
                    print("P", end=" ")
                elif (r, c) in self.ghost_position:
                    print("G", end=" ") 
                elif(self.layout[r][c] == 0 ):
                    print("_",end = " ")
                elif(self.layout[r][c] == 1):
                    print("#",end = " ")
                elif(self.layout[r][c] == 2):
                    print(".",end = " ")
                elif(self.layout[r][c] == 3):
                    print("*",end = " ")
                c = c + 1
            r = r + 1
            print()
        print()

    def handle_interactions(self, position):
        row , col = position
        if(self.layout[row][col] == 2):
            self.scores = self.scores + 1
            self.layout[row][col] = 0
            self.pacman_position = position
            print("A dot eaten !")
            print("score : ", self.scores)
            self.pacman_position = position
        elif(self.layout[row][col]== 3):
            self.power_up = True
            self.power_up_duration = 3
            self.layout[row][col] = 0
            self.pacman_position = position
            print("Power Up !!! ")
            print("Duration of power Up id : " , self.power_up_duration)
            self.pacman_position = position
        elif(self.layout[row][col] == 1):
            print("Cannot Moved ! A WAll here ")
 
    def ghost_collision(self,position):
        if position in self.ghost_position:
            if(self.power_up == True):
                self.pacman_position = position
                self.ghost_position.remove(position)
                print(" A Ghost Eaten ! ")
                return
            else:
                self.ghost_position.remove(position)
                self.lives = self.lives - 1
                print("collision with Ghost remaining lives : ",self.lives)
                return
        r , c = position
        if(self.layout[r][c] == 0):
            self.pacman_position = position

    def is_validmove(self , position):
        r, c = position
        if(r < len(self.layout) and r >= 0 and c < len(self.layout[r]) and c >= 0 ):
            return True
        return False

    def move_to_position(self,direction):
        if(self.lives <= 0):
            print("Game Over \n")
            self.display()
            return False
        row, col = self.pacman_position
        new_position = self.pacman_position
        if(direction == "up"):
            new_position = (row - 1, col)
        elif(direction == "down"):
            new_position = (row + 1, col)
        elif(direction == "left"):
            new_position = (row , col - 1)
        elif(direction == "right"):
            new_position = (row , col + 1)  
        if(self.is_validmove(new_position)):
            self.handle_interactions(new_position)
            self.ghost_collision(new_position)
            self.update()
            self.move_ghost()
            self.display()
            return True
     
    def update(self):
        if(self.power_up == True):
            self.power_up_duration = self.power_up_duration - 1
            if(self.power_up_duration <= 0):
                self.power_up = False
                print("Power Up Expired !")
            else:
                print("Power Up duration Left : " , self.power_up_duration)

    def result(self):
        print()
        print("scores : ",self.scores)
        print("Lives : ", self.lives )
        print("is power up on ", self.power_up)
        print("power up duration : ",self.power_up_duration)
        print()
        
    def check_dot(self):
        a = True
        for x in self.layout:
            for y in x:
                if(y == 2):
                    a = False
        if(a == True):
            return True
        return False

layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 2, 0, 1, 1, 0, 0, 1],
    [1, 3, 1, 1, 3, 0, 1, 1, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

m = Maze(layout)
m.display()
while(m.lives):
    p = input("enter position ( up , left , down ,right ) : ")
    m.move_to_position(p)
    if(m.check_dot()):
       print("you ate all dots.   Winner!")
       m.result()
       break
if(not m.lives):
    print("Game Over !")
    m.result()
