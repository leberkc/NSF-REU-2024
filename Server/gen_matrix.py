import random
from random import sample
import numpy as np

#K=12
#random.seed(K)
#distribution = mu

    
def generate_matrix(G, distribution, num_messages, K):

     #Ensure that one message is not encoded as per LT algorithm
     #If no single plain text message exists, for message i, then make G[i][i] = 1 
    random.seed(K)
    count = 0   #keep track of the number of unencoded messages
    random_message_pairs = random.choices(num_messages, distribution, k=K)
    for i in range(len(G)):
        message_pairs = sample(num_messages, random_message_pairs[i])
        unique_pairs = set(message_pairs) # get unique values in list
        message_pairs = list(unique_pairs)
        if not message_pairs:
           G[i][i] = 1
           count +=  1
           continue
        for j in range(len(message_pairs)):
            G[i][message_pairs[j]] = 1
            if len(message_pairs) == 1:
                count +=  1
    return G
  
def G_Matrix(K, probs):
    num_messages = list(range(0,K))
    G= np.zeros((len(num_messages),len(num_messages)))
    G_mat = generate_matrix(G, probs, num_messages, K)
    return G_mat 