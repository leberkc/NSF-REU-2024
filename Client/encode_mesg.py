# The function get_mesg_pairs returns a dictionary of messages as keys and which other
# messages are XOR'd from the G matrix as values
def get_mesg_pairs(G):  
    mesg_pairs = {}       
    for i in range(len(G)):  # number of rows
        xor_row_list = []
        for j in range(len(G)):  # of columns
            if G[i][j] == 1:
                xor_row_list.append(j)
            mesg_pairs[i] = xor_row_list
    return mesg_pairs

    
def xor(m, blocks, K, bs): # xor all elements in mesg_pairs list
    t = []  # create the list to store the encoded blocks for the message (i.e. test_file3.txt)
    first_block = blocks[1]
    last_block = blocks[K-1]
    count = 0
    for k, v in m.items():
        if len(v)-1 == 0:
            plain_text_mesg = blocks[k]             # only 1 block in the list
            count += 1                                   # so do not do encode! Just
                                                         # store it as plain text
            t.append(plain_text_mesg)                    # message in list, t
            continue
           
        for j in range(len(v)-1):

        # XOR only works if files are the same size.  If XOR a two different sized files
        # we pad the smaller file with 0's to make them the same size
        # We can make it the same size as the first block (split_files[1])
        # since we know it will alway occupy the entire block
        # We just make sure to avoid the case where the only block in the random_pairs list
        # is the last block.  We send this as plain text and dont need to encode it
        # or any message which only has a single pair in the random_pairs list
        # This usually happens with the last block if it doesnt fill the entire block
        # and any XOR pair that includes the last block

            if len(blocks[v[j]]) < bs and len(v) > 1:  # make sure not XOR single block
                                                             # with itself
                                                          
                blocks[v[j]] = [l | r for (l, r) in itertools.zip_longest(blocks[v[j]], blocks[1], fillvalue=0)]
                xor_encode = blocks[v[j]]
                next_mesg = blocks[v[j+1]]
 
            else:                                               # If there is more than
                                                                # 1 pair in the list
                                                                # encode them!
                xor_encode = blocks[v[j]]
                next_mesg = blocks[v[j+1]]

            xor_encode = bytes(a ^ b for (a,b) in zip(xor_encode,next_mesg))
        t.append(xor_encode)  # contains the encoded blocks for each 1KB block from the 11 KB file test_file3.txt
    return t
    
def encode(G, blocks, K, bs) :
    m = get_mesg_pairs(G)
    t = xor(m, blocks, K, bs)
    return t
