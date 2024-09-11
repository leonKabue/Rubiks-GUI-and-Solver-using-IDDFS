from collections import deque
import copy
import random

def faces(index):
    face = ["red", "blue", "orange", "green", "white", "yellow"]
    return face[index]


def create_rubik(n):
    cube = []
    for face in range(6):
        cube.append([[faces(face)] * n for i in range(n)])
    return Rubik(cube)


class Rubik(object):
    def __init__(self, cube):
        self.cube = list(cube[:])
        self.length = len(cube[0])
                    
    def get_cube(self):
        return self.cube[:]
    
    def get_length(self):
        return self.length
    
    def get_front(self):
        return self.cube[0][:]
    
    def get_left(self):
        return self.cube[1][:]
    
    def get_back(self):
        return self.cube[2][:]
    
    def get_right(self):
        return self.cube[3][:]
    
    def get_up(self):
        return self.cube[4][:]
    
    def get_down(self):
        return self.cube[5][:]
        
    def reset(self):
        n = self.length
        self.cube = []
        for face in range(6):
            self.cube.append([[faces(face)] * n for i in range(n)])
    
    def successors(self):
        moves = ["up", "down", "right", "left", "front", "back",
                "up^", "down^", "right^", "left^", "front^", "back^"]
        
        for move in moves:
            cube = self.copy()
            cube.perform_move(move)
            yield move, cube

    def perform_move(self, move):
        n = self.length
        
        if move == "up":
            new = self.cube[3][0][:]
            for face in range(4):
                old = self.cube[face][0][:]
                self.cube[face][0] = new[:]
                new = old[:]
            
            up = self.get_up()[:]
            side1 = up[0][:]
            side2 = [up[n-x-1][n-1] for x in range(n)][:]
            side3 = up[n-1][:]
            side4 = [up[n-x-1][0] for x in range(n)][:]
            
            self.cube[4][0] = side4[:]
            for i in range(n):
                self.cube[4][i][n-1] = side1[i]
            self.cube[4][n-1] = side2[:]
            for i in range(n):
                self.cube[4][i][0] = side3[i]
            return True

        elif move == "down":
            n = len(self.cube[0])
            new = self.cube[0][n-1][:]
            for face in range(3 ,-1, -1):
                old = self.cube[face][n-1][:]
                self.cube[face][n-1] = new[:]
                new = old[:]
            
            down = self.get_down()[:]
            side1 = down[0][:]
            side2 = [down[n-x-1][n-1] for x in range(n)][:]
            side3 = down[n-1][:]
            side4 = [down[n-x-1][0] for x in range(n)][:]
            
            self.cube[5][0] = side4[:]
            for i in range(n):
                self.cube[5][i][n-1] = side1[i]
            self.cube[5][n-1] = side2[:]
            for i in range(n):
                self.cube[5][i][0] = side3[i]
            return True

        elif move == "right":
            side1 = [self.cube[0][x][n-1] for x in range(n)]
            side2 = [self.cube[4][n-x-1][n-1] for x in range(n)]
            side3 = [self.cube[2][n-x-1][0] for x in range(n)]
            side4 = [self.cube[5][x][n-1] for x in range(n)]
            
            for i in range(n):
                self.cube[0][i][n-1] = side4[i]
            for i in range(n):
                self.cube[4][i][n-1] = side1[i]
            for i in range(n):
                self.cube[2][i][0] = side2[i]
            for i in range(n):
                self.cube[5][i][n-1] = side3[i]

            right = self.cube[3][:]
            side1 = right[0][:]
            side2 = [right[n-x-1][n-1] for x in range(n)][:]
            side3 = right[n-1][:]
            side4 = [right[n-x-1][0] for x in range(n)][:]
            
            self.cube[3][0] = side4[:]
            for i in range(n):
                self.cube[3][i][n-1] = side1[i]
            self.cube[3][n-1] = side2[:]
            for i in range(n):
                self.cube[3][i][0] = side3[i]
            return True

        elif move == "left":
            side1 = [self.cube[0][x][0] for x in range(n)]
            side2 = [self.cube[5][n-x-1][0] for x in range(n)]
            side3 = [self.cube[2][n-x-1][n-1] for x in range(n)]
            side4 = [self.cube[4][x][0] for x in range(n)]

            for i in range(n):
                self.cube[0][i][0] = side4[i]
            for i in range(n):
                self.cube[5][i][0] = side1[i]
            for i in range(n):
                self.cube[2][i][n-1] = side2[i]
            for i in range(n):
                self.cube[4][i][0] = side3[i]

            left = self.cube[1][:]
            side1 = left[0][:]
            side2 = [left[n-x-1][n-1] for x in range(n)][:]
            side3 = left[n-1][:]
            side4 = [left[n-x-1][0] for x in range(n)][:]
            
            self.cube[1][0] = side4[:]
            for i in range(n):
                self.cube[1][i][n-1] = side1[i]
            self.cube[1][n-1] = side2[:]
            for i in range(n):
                self.cube[1][i][0] = side3[i]
            return True

        elif move == "front":
            side1 = [self.cube[3][n-x-1][0] for x in range(n)]
            side2 = [self.cube[5][0][x] for x in range(n)]
            side3 = [self.cube[1][n-x-1][n-1] for x in range(n)]
            side4 = self.cube[4][n-1][:]

            for i in range(n):
                self.cube[3][i][0] = side4[i]
            for i in range(n):
                self.cube[5][0][i] = side1[i]
            for i in range(n):
                self.cube[1][i][n-1] = side2[i]
            for i in range(n):
                self.cube[4][n-1][i] = side3[i]

            front = self.cube[0][:]
            side1 = front[0][:]
            side2 = [front[n-x-1][n-1] for x in range(n)][:]
            side3 = front[n-1][:]
            side4 = [front[n-x-1][0] for x in range(n)][:]
            
            self.cube[0][0] = side4[:]
            for i in range(n):
                self.cube[0][i][n-1] = side1[i]
            self.cube[0][n-1] = side2[:]
            for i in range(n):
                self.cube[0][i][0] = side3[i]
            return True
        
        elif move == "back":
            side1 = [self.cube[3][x][n-1] for x in range(n)]
            side2 = [self.cube[4][0][n-x-1] for x in range(n)]
            side3 = [self.cube[1][x][0] for x in range(n)]
            side4 = [self.cube[5][n-1][n-x-1] for x in range(n)]

            for i in range(n):
                self.cube[3][i][n-1] = side4[i]
            for i in range(n):
                self.cube[4][0][i] = side1[i]
            for i in range(n):
                self.cube[1][i][0] = side2[i]
            for i in range(n):
                self.cube[5][n-1][i] = side3[i]

            back = self.cube[2][:]
            side1 = back[0][:]
            side2 = [back[n-x-1][n-1] for x in range(n)][:]
            side3 = back[n-1][:]
            side4 = [back[n-x-1][0] for x in range(n)][:]
            
            self.cube[2][0] = side4[:]
            for i in range(n):
                self.cube[2][i][n-1] = side1[i]
            self.cube[2][n-1] = side2[:]
            for i in range(n):
                self.cube[2][i][0] = side3[i]
            return True
            
        elif move == "up^":
            new = self.cube[0][0][:]
            for face in range(3, -1, -1):
                old = self.cube[face][0][:]
                self.cube[face][0] = new[:]
                new = old[:]
            
            up = self.get_up()[:]
            side1 = [up[0][n-x-1] for x in range(n)][:]
            side2 = [up[x][n-1] for x in range(n)][:]
            side3 = [up[n-1][n-x-1] for x  in range(n)][:]
            side4 = [up[x][0] for x in range(n)][:]
            
            self.cube[4][0] = side2[:]
            for i in range(n):
                self.cube[4][i][n-1] = side3[i]
            self.cube[4][n-1] = side4[:]
            for i in range(n):
                self.cube[4][i][0] = side1[i]
            return True

        elif move == "down^":
            n = len(self.cube[0])
            new = self.cube[3][n-1][:]
            for face in range(0 ,4):
                old = self.cube[face][n-1][:]
                self.cube[face][n-1] = new[:]
                new = old[:]
            
            down = self.get_down()[:]
            side1 = [down[0][n-x-1] for x in range(n)][:]
            side2 = [down[x][n-1] for x in range(n)][:]
            side3 = [down[n-1][n-x-1] for x  in range(n)][:]
            side4 = [down[x][0] for x in range(n)][:]
            
            self.cube[5][0] = side2[:]
            for i in range(n):
                self.cube[5][i][n-1] = side3[i]
            self.cube[5][n-1] = side4[:]
            for i in range(n):
                self.cube[5][i][0] = side1[i]
            return True

        elif move == "right^":
            side1 = [self.cube[0][x][n-1] for x in range(n)]
            side2 = [self.cube[4][x][n-1] for x in range(n)]
            side3 = [self.cube[2][n-x-1][0] for x in range(n)]
            side4 = [self.cube[5][n-x-1][n-1] for x in range(n)]
            
            for i in range(n):
                self.cube[0][i][n-1] = side2[i]
            for i in range(n):
                self.cube[4][i][n-1] = side3[i]
            for i in range(n):
                self.cube[2][i][0] = side4[i]
            for i in range(n):
                self.cube[5][i][n-1] = side1[i]

            right = self.get_right()[:]
            side1 = [right[0][n-x-1] for x in range(n)][:]
            side2 = [right[x][n-1] for x in range(n)][:]
            side3 = [right[n-1][n-x-1] for x  in range(n)][:]
            side4 = [right[x][0] for x in range(n)][:]
            
            self.cube[3][0] = side2[:]
            for i in range(n):
                self.cube[3][i][n-1] = side3[i]
            self.cube[3][n-1] = side4[:]
            for i in range(n):
                self.cube[3][i][0] = side1[i]
            return True

        elif move == "left^":
            side1 = [self.cube[0][x][0] for x in range(n)]
            side2 = [self.cube[5][x][0] for x in range(n)]
            side3 = [self.cube[2][n-x-1][n-1] for x in range(n)]
            side4 = [self.cube[4][n-x-1][0] for x in range(n)]

            for i in range(n):
                self.cube[0][i][0] = side2[i]
            for i in range(n):
                self.cube[5][i][0] = side3[i]
            for i in range(n):
                self.cube[2][i][n-1] = side4[i]
            for i in range(n):
                self.cube[4][i][0] = side1[i]

            left = self.get_left()[:]
            side1 = [left[0][n-x-1] for x in range(n)][:]
            side2 = [left[x][n-1] for x in range(n)][:]
            side3 = [left[n-1][n-x-1] for x  in range(n)][:]
            side4 = [left[x][0] for x in range(n)][:]
            
            self.cube[1][0] = side2[:]
            for i in range(n):
                self.cube[1][i][n-1] = side3[i]
            self.cube[1][n-1] = side4[:]
            for i in range(n):
                self.cube[1][i][0] = side1[i]
            return True

        elif move == "front^":
            side1 = [self.cube[3][x][0] for x in range(n)][:]
            side2 = [self.cube[5][0][n-x-1] for x in range(n)][:]
            side3 = [self.cube[1][x][n-1] for x in range(n)][:]
            side4 = [self.cube[4][n-1][n-x-1] for x in range(n)][:]

            for i in range(n):
                self.cube[3][i][0] = side2[i]
            for i in range(n):
                self.cube[5][0][i] = side3[i]
            for i in range(n):
                self.cube[1][i][n-1] = side4[i]
            for i in range(n):
                self.cube[4][n-1][i] = side1[i]

            front = self.get_front()[:]
            side1 = [front[0][n-x-1] for x in range(n)][:]
            side2 = [front[x][n-1] for x in range(n)][:]
            side3 = [front[n-1][n-x-1] for x  in range(n)][:]
            side4 = [front[x][0] for x in range(n)][:]
            
            self.cube[0][0] = side2[:]
            for i in range(n):
                self.cube[0][i][n-1] = side3[i]
            self.cube[0][n-1] = side4[:]
            for i in range(n):
                self.cube[0][i][0] = side1[i]
            return True
        
        elif move == "back^":
            side1 = [self.cube[3][n-x-1][n-1] for x in range(n)]
            side2 = [self.cube[4][0][x] for x in range(n)]
            side3 = [self.cube[1][n-x-1][0] for x in range(n)]
            side4 = [self.cube[5][n-1][x] for x in range(n)]

            for i in range(n):
                self.cube[3][i][n-1] = side2[i]
            for i in range(n):
                self.cube[4][0][i] = side3[i]
            for i in range(n):
                self.cube[1][i][0] = side4[i]
            for i in range(n):
                self.cube[5][n-1][i] = side1[i]

            back = self.get_back()[:]
            side1 = [back[0][n-x-1] for x in range(n)][:]
            side2 = [back[x][n-1] for x in range(n)][:]
            side3 = [back[n-1][n-x-1] for x  in range(n)][:]
            side4 = [back[x][0] for x in range(n)][:]
            
            self.cube[2][0] = side2[:]
            for i in range(n):
                self.cube[2][i][n-1] = side3[i]
            self.cube[2][n-1] = side4[:]
            for i in range(n):
                self.cube[2][i][0] = side1[i]
            return True
   
    def copy(self):
        return Rubik(copy.deepcopy(self.get_cube()))
    
    def is_solved(self):
        n = self.length
        for face in range(6):
            for row in range(n):
                for col in range(n):
                    if faces(face) != self.cube[face][row][col]:
                        return False
        return True
    
    def scramble(self, n):
        moves = ["up", "down", "right", "left", "front", "back",
                "up^", "down^", "right^", "left^", "front^", "back^"]
        for i in range(n):
            self.perform_move(random.choice(moves))

    def find_solution(self, limit):
        if self.is_solved():
            return []
        for lim in range(limit):
            sln = self.iddfs_helper(lim)
            if len(sln) > 0:
                for move in sln:
                    yield move
                return
    
    def iddfs_helper(self, limit):
        frontier  = deque()
        
        visited =  set()
        
        parents = {}
        
        initial = self.copy()
        
        frontier.append(initial)
        
        parents[initial.get_tuple()] = (0, [])
    
        while(len(frontier)) > 0:
            rubik = frontier.pop()
            lim, moves = parents[rubik.get_tuple()]
            
            if rubik.is_solved():
                return moves
            if lim <= limit:
                for move, cube  in rubik.successors():
                    if cube.is_solved():
                        cubeMoves = moves[:]
                        cubeMoves.append(move)
                        return cubeMoves[:]
                    cube_tuple = cube.get_tuple()
                    if cube_tuple not in visited:
                        visited.add(cube_tuple)
                        cubeMoves = moves[:]
                        cubeMoves.append(move)
                        parents[cube_tuple] = (lim+1, cubeMoves[:])
                        frontier.append(cube)
        return []

    def get_tuple(self):
        tpl = []
        for face in range(len(self.cube)):
            fce = []
            for lst in self.cube[face]:
                fce.append(tuple(lst))
            tpl.append(tuple(fce))
        return tuple(tpl)
