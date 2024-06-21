from collections import deque
import copy
from soliton import probabilities
from gen_matrix import G_Matrix

encoded_message = [b'\x03', b'\x17', b'{', b'\x03', b'\x08', b'\x04', b'w', b'\r', b'H', b'\x00', b'd']  # w/ changed xor_pairs
xor_pairs = {0: [2, 4], 1: [1, 8], 2: [0, 6, 10], 3: [7, 9], 4: [2, 10], 5: [0, 9], 6: [6], 7: [0, 1], 8: [0, 5], 9: [3, 9], 10: [10]}
mat = [[0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,],
 [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,],
 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,],
 [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 #[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,], # change from (0,3) to (0,5)
 [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,], 
 [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,]]


def receive_packet(able_to_decode, sent_token):
    while True:
        token_id_input = input("To send an encoded message, enter a token id between 0 to 10 or type q to quit: ")
        if token_id_input.lower() == 'q': return None
        try:
            token_id = int(token_id_input)
            if 0 <= token_id < len(encoded_message):
                break
            else:
                print("Must be between 0 to 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 10.")
    sent_token[token_id] = encoded_message[token_id]

    if row_sum[token_id] == 1 and mat[token_id][token_id] == 1: #if given token is plaintext
        is_plaintext = sent_token[token_id].decode('utf-8')
        if is_plaintext.isalpha() or is_plaintext.isnumeric(): #if that tokens plaintext is letter or number
            decoded_message[token_id] = encoded_message[token_id].decode()
            update_dependencies(token_id, updated_row_sum, able_to_decode, sent_token)
    else:
        check_dependencies(able_to_decode, sent_token)
    return token_id


def update_dependencies(token_id, updated_row_sum, able_to_decode, sent_token):
    for row_id in range(len(mat)):
        if updated_mat[row_id][token_id] == 1:
            updated_mat[row_id][token_id] = 0
    updated_row_sum.clear()
    updated_row_sum.extend(map(sum, updated_mat))
    check_dependencies(able_to_decode, sent_token)


def check_dependencies(able_to_decode, sent_token):
    for i in range(len(updated_row_sum)):
        if updated_row_sum[i] == 1 and i not in able_to_decode and sent_token[i]: #Row dependency is 1 and it's not plaintext
            able_to_decode.append(i)


def decode(token_id):
    pair = xor_pairs.get(token_id)
    byte1 = sent_token[token_id] 
    bytes2 = []
    letter_index = None
    for index in pair:
        if decoded_message[index] is not None:
            bytes2.append(bytes([ord(decoded_message[index])]))
        else:
            letter_index = index
    result = bytearray()
    for byte_sequence in bytes2:
        if isinstance(byte_sequence, str):
            byte_sequence = byte_sequence.encode('utf-8')
        byte1 = bytes(a ^ b for a, b in zip(byte1, byte_sequence))
    result = byte1
    print(result)
    decoded_message[letter_index] = result.decode()
    update_dependencies(letter_index, updated_row_sum, able_to_decode, sent_token)


def begin_decoding(encoded_message):
    num_tokens = len(encoded_message)
    sent_token = [None]*num_tokens
    decoded_message = [None]*num_tokens
    
    K = len(encoded_message)
    probs = probabilities(K)
    
    mat = G_Matrix(K, probs)
    for row in mat:
    	print(row)
    	
    row_sum  = list(map(sum, mat))
    updated_mat = copy.deepcopy(mat)
    updated_row_sum = copy.deepcopy(row_sum)
    able_to_decode = deque()

    while sum(updated_row_sum) != 0:
        token_id = receive_packet(able_to_decode, sent_token)
        if token_id is None:
            break
        while able_to_decode:
            packet_index = able_to_decode.popleft()
            decode(packet_index)
        
        print("Updated matrix:")
        for row in updated_mat:
            print(row)
        print("Updated row sums:", updated_row_sum)
        print("Able to decode:", list(able_to_decode))
        print("Sum: " + str(sum(updated_row_sum)))
        print("Decoded message: ", decoded_message)
        print("Sent tokens: ", sent_token)
"""
