import sys
import time


# Original output
OUT = sys.stdout
LEFT = 1
RIGHT = 0
TERMINAL_STATE = None

class CONSTANTS:
	def __init__(self, missionaries, cannibals):
		self.MAX_M = missionaries
		self.MAX_C = cannibals
		

class State:

	def __init__(self, missionaries, cannibals, dir, mis_passed, can_passed, CONSTS,moves):
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.dir = dir
		self.mis_passed = mis_passed
		self.can_passed = can_passed
		self.CONSTANTS = CONSTS
		self.moves = moves
		self.action = ""
		

	def adjacent_edges(self):
		list_child = []
		if not self.is_valid() or self.is_goal():
			return list_child

		sgn , direction = [-1 ,"left -> right"]  if self.dir == LEFT else [1,"left <- right"] 

		for i in self.moves:
			(m, c) = i
			if sgn == 1: # Right
				new_state = State(self.missionaries +  m, 
								self.cannibals +  c,
								self.dir +  1,
								self.mis_passed -  m, 
								self.can_passed -  c,
								self.CONSTANTS,self.moves)
			else : #Left
				new_state = State(self.missionaries - m, 
								self.cannibals - c,
								self.dir - 1,
								self.mis_passed + m, 
								self.can_passed + c,
								self.CONSTANTS,self.moves)
			if new_state.is_valid():
				new_state.action = "%d missionaries and %d cannibals %s." % (m, c, direction)
				list_child.append(new_state)
		return list_child

	def is_goal(self):
		return self.cannibals == 0 and self.missionaries == 0 and self.dir == RIGHT

	def is_valid(self):
		if self.missionaries < 0 or self.cannibals < 0  or (
				self.dir != 0 and self.dir != 1):
			return False
		if self.missionaries > self.CONSTANTS.MAX_M or \
			self.cannibals > self.CONSTANTS.MAX_C:
			return False

		if (self.cannibals > self.missionaries > 0) or (
				self.can_passed > self.mis_passed > 0): 
			return False

		return True

	
	def __str__(self):
		return "\nState (%d, %d, %d, %d, %d)\n%s" % (
			self.missionaries, self.cannibals, self.dir, self.mis_passed,
			self.can_passed,self.action)




class Graph:

	def __init__(self):
		self.bfs_parent = {}
		self.dfs_parent = {}
		self.visited_dfs=0
		self.visited_bfs={}
		

	def dfs_util(self, u,visited):

		visited[(u.missionaries, u.cannibals, u.dir)] = True
		self.visited_dfs += 1

		if u.is_goal():
			self.dfs_parent[TERMINAL_STATE] = u
			return True 

		for v in u.adjacent_edges():
			if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
				self.dfs_parent[v] = u
				path = self.dfs_util(v,visited)
				if path :
					return True
		return False
				
				

	def DFS(self, s):
			self.dfs_parent[s] = None
			self.visited_dfs = 0
			visited={(s.missionaries, s.cannibals, s.dir): True}
			self.dfs_util(s,visited)							
			return self.dfs_parent



	def BFS(self, s):
		self.bfs_parent[s] = None
		self.visited_bfs = {(s.missionaries, s.cannibals, s.dir): True}
		
		queue = [s]
		while queue:
			u = queue.pop(0)

			if u.is_goal():
				self.bfs_parent[TERMINAL_STATE] = u
				queue.clear()
				return self.bfs_parent

			for v in u.adjacent_edges():
				if (v.missionaries, v.cannibals, v.dir) not in self.visited_bfs.keys():
					self.bfs_parent[v] = u
					queue.append(v)
					self.visited_bfs[(v.missionaries, v.cannibals, v.dir)] = True
					
		return {}

	
	def print_path(self, path, tail):
		if path == {} or path is None or tail is None:  
			print("No Solution")
			return
		if tail == TERMINAL_STATE:
			tail = path[tail]
		stack = []
		parent = tail
		while parent is not None:
			stack.append(parent)
			parent = path[parent]

		while stack:
			print(stack.pop())


def possible_moves(capacity):
	# Possible moves for spefic numbers of missionares and cannibals
	moves = []
	for m in range(capacity + 1):
		for c in range(capacity + 1):
			if (1 <= m + c <= capacity) and not ( 0< m < c):
				moves.append((m, c))

	return moves



if __name__ == '__main__':
	
	inputs = sys.argv
	
	m = int(inputs[1]) 
	c = int(inputs[2])
	k = int(inputs[3])
	
	if m <0 or c <0 :
		print("Wrong inputs(negative numbers)")

	CNST = CONSTANTS(m, c)
	moves = possible_moves(k)

	INITIAL_STATE = State(CNST.MAX_M, CNST.MAX_C, LEFT, 0, 0, CNST, moves) 
	TERMINAL_STATE = State(-1, -1, RIGHT, -1, -1,CNST,None)
	

	g = Graph() #Make the graph 
	#------------------------------------------------- For BFS solution-----------------------------------------------

	sys.stdout = OUT
	print("\nRunning BFS...")
	sys.stdout = open("out_BFS.txt", "w")

	start_time = time.time()
	g.print_path(g.BFS(INITIAL_STATE), TERMINAL_STATE) #BFS return the path
	end_time = time.time()
	print("\nExecution time in BFS: %.2fms" % ((end_time - start_time)*1000))
	sys.stdout = OUT
	print("Explored Nodes: " + str(g.visited_bfs.__len__()))
	print("Finish BFS!")

	#------------------------------------------------- For DFS solution-----------------------------------------------
	print("\nRunning DFS...")
	sys.stdout = open("out_DFS.txt", "w")

	start_time = time.time()
	g.print_path(g.DFS(INITIAL_STATE), TERMINAL_STATE) #DFS return the path
	end_time = time.time()
	print("\nExecution time in DFS: %.2fms" % ((end_time - start_time)*1000))
	sys.stdout = OUT
	print("Explored Nodes: " + str(g.visited_dfs))
	print("Finish DFS!")


