import sys
import numpy as np
import scipy.sparse as sps

#display setting so numpy can display the whole matrix in the terminal
np.set_printoptions(threshold=sys.maxsize)

#number of users
size = 4

#initialize adjacency matrix
adjacency_matrix = [[0 for i in range(size)] for j in range(size)]

# i place is for the opinion of i node with range [-1,1]
#s_opinion_vector = np.array([0,0,0,0,0,0,0,0,0,1,0,0,0,
	#0,1,1,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1])
s_opinion_vector = np.array([-1,0,1,-1])
#open the karate datafile
with open('test.txt') as fp:
	#read line by line
	for cnt, line in enumerate(fp):
		#connections in the datafile start after the '%' symbol
		if(line[0]!='%'):
			users = line.split(" ")
			#turn them into integers and strip the newline
			user1 = int(users[0])
			user2 = int(users[1].rstrip())
			#users are defined from 0 to 5
			#-1 if users defined from index 1
			#so that each user is the same with his index
			adjacency_matrix[user1][user2]=1
			#non directed graph
			adjacency_matrix[user2][user1]=1


#print the matrix
#print(np.matrix(adjacency_matrix))

n,m = np.matrix(adjacency_matrix).shape
diags = np.matrix(adjacency_matrix).sum(axis=1)
D = sps.spdiags(diags.flatten(), [0], m, n, format='csr')

laplacian_matrix = (np.matrix(D - np.matrix(adjacency_matrix)))

#size of adj matrix
identity_matrix = np.identity(size)

laplacian_plus_identity =  identity_matrix.__add__(laplacian_matrix)


fundamental_matrix = np.linalg.inv(laplacian_plus_identity)

#print(fundamental_matrix)

z_vector = fundamental_matrix.dot(s_opinion_vector)

#print(z_vector)

# divided with the size
polarization_index = np.linalg.norm(z_vector)/size

print(polarization_index)









