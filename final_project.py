from collections import defaultdict
from itertools import chain
import random
import math
import hashlib
import time


def initPlyColor(colors,userFirst):
    select_color=''
    another_color=''
    ply_colors = {}

    select_color = input('Enter your color B/R:') if userFirst else random.choice(colors)
    for color in colors:
        if color != select_color:
            another_color = color
            break

    ply_colors['ply_move'] = select_color if userFirst else another_color
    ply_colors['AI_move'] = select_color if not userFirst else another_color
    
    return ply_colors

def plyLoop(pre_state):
    plyMove = plySelectTile(pre_state.board)
    ply_state = pre_state.next_state(plyMove)
    ply_state.printBoard(ply_state.move_board,plyMove)
    ply_state.printBoard(ply_state.board)

    #check terminal
    final_board = ply_state.board if ply_state.terminal() else ''
    return ply_state,final_board

def AILoop(pre_state):
    #AI turn
    K = 1000  # MCTS training iteration
    ply_node = Node(pre_state)
    AI_state = UCTSEARCH(K,ply_node).state
    
    AI_state.printBoard(AI_state.move_board,AI_state.pre_move)
    AI_state.printBoard(AI_state.board)
    
    #check terminal
    final_board = AI_state.board if AI_state.terminal() else ''
    return AI_state,final_board

def plySelectTile(board):
    global size
    legal = False
    
    #check legal
    ## user inpu12t 長度要是 2
    ## 只能從board裡面選
    ## 不能移別人的顏色
    while not legal:
        row = input('User => enter a row : ')
        col = input('User => enter a col : ')
        tileIndex = (int(row)-1,int(col)-1)

        if size<10 and (len(row)!=1 or len(col)!=1):
            print('illegal move , must enter 2 numbers.')
            continue
        else:
            tileColor = board[tileIndex[0]][tileIndex[1]]
            if tileColor == 'X':
                print('illegal move , can not choose a empty space.')
                continue
            else:
                if tileColor != ply_colors['ply_move']:
                    print('illegal move , can not choose the enemy color.')
                    continue
                else:
                    legal = True
    
    return tileIndex

class State(): 
    win = 0
    titles = {
        'ply_move' : r'user move (%d,%d) : %s',
        'AI_move' :  r'AI move (%d,%d) : %s',
        'AI_side_effect' : r'side effect',
    }
    side_tiles = []

    def __init__(self,board,color={},move_state='',steps=0,pre_move='',side_panalty=0,move_board=''):
        self.board = board
        self.move_board = move_board
        self.board_size = len(board)
        self.steps = steps
        self.color = color
        self.pre_move = pre_move
        self.side_panalty = side_panalty
        self.move_state = move_state
        next_move_state = 'ply_move' if self.move_state == 'AI_move' else 'AI_move'
        self.moves = [(i//self.board_size,i%self.board_size)for i,tile in enumerate(list(chain(*board))) if tile == color[next_move_state]] # possible moves

    def next_state(self,next_move=''):
        self.steps += 1
        nextMove = next_move if next_move else random.choice(self.moves) #one tile
        move_board = self.remove(self.board,[nextMove])
        new_board = self.sideEffect(move_board,nextMove)
        next_move_state = 'ply_move' if self.move_state == 'AI_move' else 'AI_move'
        
        next_side_panalty = self.sidePanalty(move_board,self.side_tiles)
        
        next_state = State(new_board,self.color,next_move_state,self.steps,nextMove,next_side_panalty,move_board) 
        return next_state

    def remove(self,board,tileIndexs):
        # tileIndex = [(i,j)...]
        new_board = [tile if (i//self.board_size,i%self.board_size) not in tileIndexs else 'X' for i,tile in enumerate(list(chain(*board)))]
        new_board = [new_board[j*self.board_size:j*self.board_size + self.board_size] for j in range(self.board_size)]                
        return new_board
    
    def sideEffect(self,board,tileIndex):
        checkTiles,wall_ctn = self.get4NeighborTiles(board,tileIndex)
        self.side_tiles = []
        for checkTile in checkTiles:
            tiles,walls = self.get4NeighborTiles(board,checkTile)    
            if len(tiles) + walls <=2:
                self.side_tiles.append(checkTile)
        return self.remove(board,self.side_tiles)

    def sidePanalty(self,board,delTiles):
        next_side_panalty = 0.0
        for tile in self.side_tiles:
            if board[tile[0]][tile[1]] == self.color['AI_move']:
                next_side_panalty += 1
            else:
                next_side_panalty -= 1
        return next_side_panalty
                
    def get4NeighborTiles(self,board,tileIndex):
        checkTiles = []
        candTiles = []
        wall_ctn = 0

        candTiles.append((tileIndex[0]-1,tileIndex[1])) #up
        candTiles.append((tileIndex[0]+1,tileIndex[1])) #down
        candTiles.append((tileIndex[0],tileIndex[1]+1)) #right
        candTiles.append((tileIndex[0],tileIndex[1]-1)) #left

        for tile in candTiles:
            if tile[0] < self.board_size and tile[0] >= 0 and tile[1] < self.board_size and tile[1] >= 0:
                if board[tile[0]][tile[1]] != 'X':
                    checkTiles.append(tile)  #還有東西的才會加進去
            else:
                wall_ctn += 1

        return checkTiles,wall_ctn
    
    def printBoard(self,board,tileIndex='',initial=''): #print 傳進來的board(可舊可新)
        title = initial if initial else self.titles[self.move_state] % (tileIndex[0]+1,tileIndex[1]+1,self.color[self.move_state]) if tileIndex else self.titles['AI_side_effect']    
        print(title +'\n')
        print('  '+ ' '.join(list(map(lambda c : str(c+1),range(self.board_size)))))
        for row,line in enumerate(board):
            print(str(row+1) + ' ' + ' '.join(line))
        print('\n')

    def terminal(self): #分出輸贏
        remainSet = list({tile for tile in list(chain(*self.board)) if tile!= 'X'})
        
        if len(remainSet) == 1: 
            self.win = -3 if remainSet[0] == self.color['AI_move'] else 3 #如果剩下的是自己的顏色，表示輸了
            return True
        elif len(remainSet) == 0: 
            self.win = -2
            return True
        return False
    
    def reward(self,MAX_STEPS):
        r = self.win
        return r        
        
    def __hash__(self):
        boardString = ' '.join(list(chain(*self.board)))
        return int(hashlib.md5(boardString.encode('utf-8')).hexdigest(),16)
    
    def __eq__(self,other):
        if hash(self)==hash(other):
            return True
        return False

class Node():
    def __init__(self, state, parent=None):
        self.visits=1
        self.reward=0.0
        self.state=state
        self.children=[]
        self.parent=parent
        
    def add_child(self,child_state):
        child=Node(child_state,self)
        self.children.append(child)
        
    def update(self,reward):
        self.reward+=reward
        self.visits+=1
        
    def fully_expanded(self):
        if len(self.children)==len(self.state.moves):
            return True
        return False
    
    def __repr__(self):
        s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)
        return s

def UCTSEARCH(budget,root):
    for iter in range(int(budget)):
        root.state.steps = 0
        front=TREEPOLICY(root)
        reward=DEFAULTPOLICY(root,front.state)
        BACKUP(front,reward)
    return BestMove(root)

def TREEPOLICY(node):
    #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    while node.state.terminal()==False:
        if len(node.children)==0:
            return EXPAND(node)
        elif random.uniform(0,1)<.5:
            node=BESTCHILD(node)
        else:
            if node.fully_expanded()==False:
                return EXPAND(node)
            else:
                node=BESTCHILD(node)
    return node

def EXPAND(node):
    tried_children=[c.state for c in node.children]
    new_state=node.state.next_state()
    while new_state in tried_children:
        new_state=node.state.next_state()
    node.add_child(new_state)
    return node.children[-1]

def BESTCHILD(node):
    scalar = 1/math.sqrt(2.0)
    bestscore=0.0
    bestchildren=[]
    for c in node.children:        
        exploit=c.reward/c.visits
        explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))
        score=exploit+scalar*explore
        if bestscore == 0.0:
            bestscore = score
        
        if score==bestscore:
            bestchildren.append(c)
        if score>bestscore:
            bestchildren=[c]
            bestscore=score
    if len(bestchildren)==0:
        print("OOPS: no best child found, probably fatal")
    return random.choice(bestchildren)

def BestMove(node):
    ###從side_panalty為正的下去選
    max_side_panalty = max([c.state.side_panalty for c in node.children])
    can_nodes = [c for c in node.children if c.state.side_panalty>=max_side_panalty]
    best_node = max(can_nodes, key=lambda c: c.reward / c.visits)
    return best_node

def DEFAULTPOLICY(root,state):
    while state.terminal()==False:
        state=state.next_state()
    MAX_STEPS = len([tile for tile in list(chain(*root.state.board)) if tile!='X'])
    return state.reward(MAX_STEPS)

def BACKUP(node,reward):
    while node!=None:
        node.visits+=1
        node.reward+=reward
        node=node.parent


# read input file
fileName = 'test_n4.txt'
board = [line.strip() for line in open(fileName,'r')]
size = int(board[0])

# get board
del board[0]
board = [line.split() for line in board]
print('initial')
print('  '+ ' '.join(list(map(lambda c : str(c+1),range(size)))))
for row,line in enumerate(board):
    print(str(row+1) + ' ' + ' '.join(line))
print('\n')

userFirst = True if input('user go first or not(Y/N):') == 'Y' else False

#get / set colors
colors = list({tile for tile in board[0]})
ply_colors = initPlyColor(colors,userFirst)  # ply_colors={'ply_move' = 'R', 'AI_move' = 'B'}

#Game loop
initState = State(board,color=ply_colors,move_state='AI_move'if userFirst else 'ply_move')
terminal = False
pre_state = ''
final_board = ''

while not terminal:
    if not pre_state:
        pre_state = initState
    
    firstLoopFunc = plyLoop if userFirst else AILoop
    secondLoopFunc = AILoop if userFirst else plyLoop

    pre_state,final_board = firstLoopFunc(pre_state)
    if final_board : break

    pre_state,final_board = secondLoopFunc(pre_state)
    if final_board : break
    
remainSet = list({tile for tile in list(chain(*final_board)) if tile!= 'X'})
message = 'user win' if (len(remainSet) == 1 and remainSet[0] == ply_colors['AI_move']) else 'AI win' if (len(remainSet) == 1 and remainSet[0] == ply_colors['ply_move']) else 'draw' 
print(message)

